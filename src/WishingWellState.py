'''
Name: Wishing Well State
Description: Here the player can obtain a tempory power increase to help with harder missions.
'''

from threading import Thread
from queue import Queue
import time
import simpleaudio as sa
from inputs import get_gamepad
from InventoryState import InventoryState
import copy

class WishingWellState:
    def __init__(self, state):
        self.state = state
        self.state.assistant.say("You stand in front of the wishing well. Make a wish for good luck!")
        self.buff_cost = self.state.player.rank * 20
        time.sleep(1)

        '''Await player action'''
        idling = True
        playerChoice = 0
        while(idling):
            playerChoice = self.handlePlayerInput()
            if playerChoice == -1:
                idling = False

    def handlePlayerInput(self):
        ''' This function handles player input in between room transitions '''
        events = get_gamepad()
        for event in events:
            if event.code == "BTN_SOUTH" and event.state == 0:
                try: 
                    if self.buff_cost > self.state.player.gold:
                        self.state.assistant.say("You don't even have a coin to spare!")
                    else:
                        wave_obj = sa.WaveObject.from_wave_file("sound effects\\chaching.wav")
                        play_obj = wave_obj.play()
                        self.state.player.effect_pool.append(["rank buff", 20])
                        self.state.player.gold -= self.buff_cost
                        self.buff_cost = self.state.player.rank * 20
                except Exception as e:
                    print(e)
                    print("purchase failed")
            elif event.code == "BTN_WEST" and event.state == 0:
                InventoryState(self.state)
                return 0
            elif event.code == "BTN_NORTH" and event.state == 0:
                self.state.assistant.say("You are standing beside the wishing well. Happy gods make happy hunts.")
                return 0
            elif event.code == "BTN_EAST" and event.state == 0:
                return -1
        return 0

if __name__ == "__main__":
    ''' Running this script as main creates a test room for the player to interact with '''
    from StateMachine import StateMachine
    state = StateMachine()
    state.player.gold = 20
    testFloor = WishingWellState(state)