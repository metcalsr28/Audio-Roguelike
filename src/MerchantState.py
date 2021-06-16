'''
Name: Merchant State
Description: Here the player can purchase potions
'''

from threading import Thread
from queue import Queue
import time
import simpleaudio as sa
from inputs import get_gamepad
from InventoryState import InventoryState
import copy

class MerchantState:
    def __init__(self, state):
        self.state = state
        self.state.assistant.say("The merchant begins showing you his wares!")
        time.sleep(.5)
        self.choice_index = 0
        self.state.assistant.say(self.state.items[self.choice_index].name)

        '''Await player action'''
        idling = True
        playerChoice = 0
        while(idling):
            playerChoice = self.handlePlayerInput()
            if playerChoice == -1:
                idling = False
    
    def toggle_selection(self, positive=True):
        if positive:
            self.choice_index += 1
            if self.choice_index == len(self.state.items):
                self.choice_index = 0
            self.state.assistant.say(self.state.items[self.choice_index].name)
        elif not positive:
            self.choice_index -= 1
            if self.choice_index < 0:
                self.choice_index == len(self.state.items) - 1
            self.state.assistant.say(self.state.items[self.choice_index].name)  

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
                    if int(self.state.items[self.choice_index].price) > self.state.player.gold:
                        self.state.assistant.say("You cannot afford that.")
                    else:
                        wave_obj = sa.WaveObject.from_wave_file("sound effects\\chaching.wav")
                        play_obj = wave_obj.play()
                        time.sleep(.5)
                        self.state.player.inventory.append(copy.copy(self.state.items[self.choice_index]))
                        self.state.player.gold -= int(self.state.items[self.choice_index].price)
                except AttributeError as e:
                    print(e)
                    print("purchase failed")
            elif event.code == "BTN_WEST" and event.state == 0:
                InventoryState(self.state)
                return 0
            elif event.code == "BTN_NORTH" and event.state == 0:
                self.state.assistant.say("You have " + str(self.state.player.gold) + " gold. One " +
                        self.state.items[self.choice_index].name + " costs " + self.state.items[self.choice_index].price + ". Would you like to purchase this item?")
                return 0
            elif event.code == "BTN_EAST" and event.state == 0:
                return -1
        return 0

if __name__ == "__main__":
    ''' Running this script as main creates a test room for the player to interact with '''
    from StateMachine import StateMachine
    state = StateMachine()
    state.player.gold = 30
    testFloor = MerchantState(state)