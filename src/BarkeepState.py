'''
Name: Barkeep STATE
Description: Here the player can pay a small fee to recover health and mana
'''

from threading import Thread
from queue import Queue
import time
import simpleaudio as sa
from inputs import get_gamepad
from InventoryState import InventoryState

class BarkeepState:
    def __init__(self, state):
        self.state = state
        self.state.assistant.say("The barkeeper asks, would you like a room bud?")
        time.sleep(.5)
        self.state.assistant.say("Yes?")
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
            self.state.assistant.say("Yes?")
        elif self.choice_index == 0:
            self.choice_index = 1
            self.state.assistant.say("No?")

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
                    if self.choice_index == 1:
                        return -1
                    else:
                        if self.state.player.gold >= 10:
                            self.state.assistant.say("The barkeep takes your money and shows you to your room.")
                            time.sleep(1)
                            wave_obj = sa.WaveObject.from_wave_file("sound effects\\sleeping.wav")
                            play_obj = wave_obj.play()
                            self.state.player.health = self.state.player.max_health
                            self.state.player.mana = self.state.player.max_mana
                            self.state.player.gold -= 10
                        else:
                            self.state.assistant.say("Insufficient funds.")
                            return 0
                except Exception as e:
                    print(e)
                    return 0
            elif event.code == "BTN_WEST" and event.state == 0:
                InventoryState(self.state)
                return 0
            elif event.code == "BTN_NORTH" and event.state == 0:
                self.state.assistant.say("You are standing in front of the barkeep. You have " + str(self.state.player.gold) + ". Would you like to rent a room for the evening?")
                return 0
            elif event.code == "BTN_EAST" and event.state == 0:
                return -1
        return 0

if __name__ == "__main__":
    ''' Running this script as main creates a test room for the player to interact with '''
    from StateMachine import StateMachine
    state = StateMachine()
    state.player.gold = 9
    testFloor = BarkeepState(state)