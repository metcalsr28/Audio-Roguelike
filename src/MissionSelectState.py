'''
Name: Mission-Select State
Description: Here the player can pay a small fee to recover health and mana
'''

from threading import Thread
from queue import Queue
import time
import simpleaudio as sa
from inputs import get_gamepad
from InventoryState import InventoryState

class MissionSelectState:
    def __init__(self, state):
        self.state = state
        self.state.assistant.say("The missions are listed in order of difficulty. They are ordered from 1 to 20. You will only be paid if you can complete the mission. \
            Please select your difficulty before accepting a mission.")
        time.sleep(1)
        self.state.assistant.say("Current difficulty," + str(self.state.difficulty))
        self.choice_index = 0

        '''Await player action'''
        idling = True
        playerChoice = 0
        while(idling):
            playerChoice = self.handlePlayerInput()
            if playerChoice == -1:
                idling = False
    
    def toggle_selection(self, positive=True):
        if self.state.on_hunt:
            wave_obj = sa.WaveObject.from_wave_file("sound effects\\big_x.wav") # Player can't adjust difficulty while on hunt.
            play_obj = wave_obj.play()
            time.sleep(1)
            return -1
        if positive:
            if self.state.difficulty != 20:
                self.state.difficulty += 1
                wave_obj = sa.WaveObject.from_wave_file("sound effects\\tink.wav")
                play_obj = wave_obj.play()
                time.sleep(.1)
        elif not positive:
            if self.state.difficulty != 1:
                self.state.difficulty -= 1             
                wave_obj = sa.WaveObject.from_wave_file("sound effects\\tink.wav")
                play_obj = wave_obj.play()
                time.sleep(.1)

    def handlePlayerInput(self):
        ''' This function handles player input in between room transitions '''
        events = get_gamepad()
        for event in events:
            
            if event.code == "ABS_Y" and event.state > 3000:
                self.toggle_selection(True)
            elif event.code == "ABS_Y" and event.state < -3000:
                self.toggle_selection(False)
            elif event.code == "BTN_SOUTH" and event.state == 0:
                if self.state.on_hunt:
                    self.state.assistant.say("You've already given your word to complete this mission. Current mission difficulty is " + str(self.state.difficulty))
                else:
                    self.state.assistant.say("You accept the mission. Current mission difficulty is " + str(self.state.difficulty))
                self.state.on_hunt = True
            elif event.code == "BTN_WEST" and event.state == 0:
                InventoryState(self.state)
                return 0
            elif event.code == "BTN_NORTH" and event.state == 0:
                self.state.assistant.say("Current difficulty, " + str(self.state.difficulty))
                return 0
            elif event.code == "BTN_EAST" and event.state == 0:
                return -1
        return 0

if __name__ == "__main__":
    ''' Running this script as main creates a test room for the player to interact with '''
    from StateMachine import StateMachine
    state = StateMachine()
    state.player.gold = 30
    testFloor = MissionSelectState(state)