'''
Name: Shrine State
Description: Here the player can buy rank ups which are synonymous with level ups from other games
'''

from threading import Thread
from queue import Queue
import time
import simpleaudio as sa
from inputs import get_gamepad
from InventoryState import InventoryState
import copy

class ShrineState:
    def __init__(self, state):
        self.state = state
        self.state.assistant.say("You enter the shrine. Give and you shall receive power in return!")
        self.rank_cost = self.state.player.rank * 50
        time.sleep(1)

        '''Await player action'''
        idling = True
        playerChoice = 0
        while(idling):
            playerChoice = self.handlePlayerInput()
            if playerChoice == -1:
                idling = False

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
            if event.code == "BTN_SOUTH" and event.state == 0:
                try: 
                    if self.rank_cost > self.state.player.gold:
                        self.state.assistant.say("You cannot afford to rank up right now.")
                    else:
                        wave_obj = sa.WaveObject.from_wave_file("sound effects\\chaching.wav")
                        play_obj = wave_obj.play()
                        self.state.player.rank_up()
                        self.state.player.gold -= self.rank_cost
                        self.rank_cost = self.state.player.rank * 50
                except:
                    print("purchase failed")
            elif event.code == "BTN_WEST" and event.state == 0:
                InventoryState(self.state)
                return 0
            elif event.code == "BTN_NORTH" and event.state == 0:
                self.state.assistant.say("Current rank, {}. You can make offerings to increase your power.".format(self.state.player.rank))
                return 0
            elif event.code == "BTN_EAST" and event.state == 0:
                return -1
        return 0

if __name__ == "__main__":
    ''' Running this script as main creates a test room for the player to interact with '''
    from StateMachine import StateMachine
    state = StateMachine()
    state.player.gold = 50
    testFloor = ShrineState(state)