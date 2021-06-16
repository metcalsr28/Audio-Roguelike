'''
Name: Outskirts State
Description: Here the player can go on hunts or challenge the grand tower
'''

from threading import Thread
from queue import Queue
import time
import simpleaudio as sa
from inputs import get_gamepad
from InventoryState import InventoryState
import copy
from HuntState import HuntState
from GrandTowerState import GrandTowerState

class OutskirtsState:
    def __init__(self, state):
        self.state = state
        self.bgm_q = Queue()
        self.bgm_thread = Thread(target=self.play_music, args=(self.bgm_q, "sound effects\\outskirts_theme.wav", True,))
        self.bgm_thread.start()
        self.state.assistant.say("You leave the town. All around you, you see dense forest. Are you headed out on a mission or are you going to challenge the tower?")
        time.sleep(.5)
        self.state.assistant.say("Hunt.")
        self.choice_index = 0

        '''Await player action'''
        idling = True
        playerChoice = 0
        while(idling):
            playerChoice = self.handlePlayerInput()
            if playerChoice == -1:
                idling = False
    
    def toggle_selection(self, positive=True):
        if self.choice_index == 1:
            self.choice_index = 0
            self.state.assistant.say("Hunt.")
        elif self.choice_index == 0:
            self.choice_index = 1
            self.state.assistant.say("Tower?")

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
                        if not self.state.on_hunt:
                            self.state.assistant.say("You need to accept a mission before you can begin your hunt.")
                            return 0
                        self.state.assistant.say("Happy hunting!")
                        time.sleep(1)
                        self.music_thread = Thread(target=self.play_music, args=(self.bgm_q, "sound effects\\hunt_theme.wav", True))
                        self.music_thread.start()
                        # enter hunt (room) state
                        HuntState(self.state)
                    elif self.choice_index == 1:
                        self.state.assistant.say("Good luck! You're going to need it.")
                        time.sleep(.5)
                        self.music_thread = Thread(target=self.play_music, args=(self.bgm_q, "sound effects\\grand_tower_theme.wav", True))
                        self.music_thread.start()
                        # enter hunt (room) state
                        GrandTowerState(self.state)
                    else:
                        raise AssertionError
                except AssertionError:
                    print("could not parse choice")
            elif event.code == "BTN_WEST" and event.state == 0:
                InventoryState(self.state)
                return 0
            elif event.code == "BTN_NORTH" and event.state == 0:
                self.state.assistant.say("You are standing on a path in the outskirts of town. If you have no business here, it's safer inside the gate.")
                return 0
            elif event.code == "BTN_EAST" and event.state == 0:
                return -1
        return 0

if __name__ == "__main__":
    from StateMachine import StateMachine
    testState = OutskirtsState(StateMachine())