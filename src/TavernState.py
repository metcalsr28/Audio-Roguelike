'''
Name: TAVERN STATE
Description: Here the player can pay a small fee to recover health and mana, as well accept hunt missions
'''

from threading import Thread
from queue import Queue
import time
import simpleaudio as sa
from inputs import get_gamepad
from InventoryState import InventoryState
from BarkeepState import BarkeepState
from MissionSelectState import MissionSelectState

class TavernState:
    def __init__(self, state):
        self.state = state
        self.bgm_q = Queue()
        self.bgm_thread = Thread(target=self.play_music, args=(self.bgm_q, "sound effects\\tavern_interior.wav", True))
        self.bgm_thread.start()
        self.state.assistant.say("You enter the tavern. The man behind the bar can sell you a room for the night, should you get exhausted from your travels. \
            On a wall nearby hangs a mission board where you can acquire bounty missions.")
        self.am_q = Queue()
        self.music_thread = Thread(target=self.play_music, args=(self.am_q, "sound effects\\innskeeper.wav", True))
        self.music_thread.start()
        time.sleep(.5)
        self.choice_index = 0

        '''Await player action'''
        idling = True
        playerChoice = 0
        while(idling):
            playerChoice = self.handlePlayerInput()
            if playerChoice == -1:
                idling = False
                self.bgm_q.put("stop")
                self.am_q.put("stop")

    def play_music(self, q, file_name, repeat=False):
        while not q.empty():
            q.get()
        if repeat:
            try:
                done = False
                while not done:
                    wave_obj = sa.WaveObject.from_wave_file(file_name)
                    play_obj = wave_obj.play()
                    while play_obj.is_playing():
                        if not q.empty():
                            if q.get() == "stop":
                                done = True
                                play_obj.stop()
                                time.sleep(1)
                                print("Stopped Sucessfully")
            except Exception as e:
                print(e)
        else:
            try:
                wave_obj = sa.WaveObject.from_wave_file(file_name)
                play_obj = wave_obj.play()
                while play_obj.is_playing():
                    if not q.empty():
                        if q.get() == "stop":
                            play_obj.stop()
                            time.sleep(1)
                            print("Stopped Sucessfully")
            except Exception as e:
                print(e)

    def toggle_selection(self, positive=True):
        if self.choice_index == 1:
            self.choice_index = 0
            self.state.assistant.say("Innskeeper?")
        elif self.choice_index == 0:
            self.choice_index = 1
            self.state.assistant.say("Mission Board?")

    def handlePlayerInput(self):
        ''' This function handles player input in between room transitions '''
        events = get_gamepad()
        for event in events:
            
            if event.code == "ABS_X" and event.state > 3000:
                self.toggle_selection(True)
            elif event.code == "ABS_X" and event.state < -3000:
                self.toggle_selection(False)
            elif event.code == "BTN_SOUTH" and event.state == 0:
                try: 
                    if self.choice_index == 0:
                        BarkeepState(self.state)
                    elif self.choice_index == 1:
                        MissionSelectState(self.state)
                    else:
                        raise AssertionError
                except:
                    print("could not parse choice")
                self.state.assistant.say("Entrance")
            elif event.code == "BTN_WEST" and event.state == 0:
                InventoryState(self.state)
                return 0
            elif event.code == "BTN_NORTH" and event.state == 0:
                self.state.assistant.say("You are standing near the tavern entrance.")
                return 0
            elif event.code == "BTN_EAST" and event.state == 0:
                return -1
        return 0

if __name__ == "__main__":
    ''' Running this script as main creates a test room for the player to interact with '''
    from StateMachine import StateMachine
    state = StateMachine()
    state.player.gold = 200
    testFloor = TavernState(state)