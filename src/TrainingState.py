'''
Name: Training State
Description: Here the player can buy magic spells
'''

from threading import Thread
from queue import Queue
import time
import simpleaudio as sa
from inputs import get_gamepad
from InventoryState import InventoryState


class TrainingState:
    def __init__(self, state):
        self.state = state
        self.state.assistant.say("The wizard agrees to teach you what he knows. For a price. Which would you like?")
        time.sleep(1)
        self.choice_index = 0
        self.state.assistant.say(self.state.spells[self.choice_index].name)

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
            if self.choice_index == len(self.state.spells):
                self.choice_index = 0
            self.state.assistant.say(self.state.spells[self.choice_index].name)
        elif not positive:
            self.choice_index -= 1
            if self.choice_index < 0:
                self.choice_index == len(self.state.spells) - 1
            self.state.assistant.say(self.state.spells[self.choice_index].name)  

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
                    if int(self.state.spells[self.choice_index].price) > self.state.player.gold:
                        self.state.assistant.say("You cannot afford that.")
                    elif self.state.spells[self.choice_index].name in self.state.player.abilities:
                        self.state.assistant.say("You already possess knowledge of that spell.")
                    else:
                        wave_obj = sa.WaveObject.from_wave_file("sound effects\\chaching.wav")
                        play_obj = wave_obj.play()
                        time.sleep(.5)
                        self.state.player.abilities.append(self.state.spells[self.choice_index].name)
                        self.state.player.gold -= int(self.state.spells[self.choice_index].price)
                except:
                    print("purchase failed")
            elif event.code == "BTN_WEST" and event.state == 0:
                InventoryState(self.state)
                return 0
            elif event.code == "BTN_NORTH" and event.state == 0:
                self.state.assistant.say("You have " + str(self.state.player.gold) + " gold. Knowledge of " +
                        self.state.spells[self.choice_index].name + " will cost you " + self.state.spells[self.choice_index].price + ". Would you like to purchase this spell?")
                return 0
            elif event.code == "BTN_EAST" and event.state == 0:
                return -1
        return 0

if __name__ == "__main__":
    ''' Running this script as main creates a test room for the player to interact with '''
    from StateMachine import StateMachine
    state = StateMachine()
    state.player.gold = 200
    testFloor = TrainingState(state)