import time
from inputs import get_gamepad
from Item import Item
class InventoryState:
    def __init__(self, state):
        self.state = state
        self.itemIndex = 0
    
    def start(self):
        self.state.assistant.say("Inventory!")
        time.sleep(.5)
        try:
            self.state.assistant.say("You have {} items, starting with {}".format(len(self.state.player.inventory), 
                                                                                self.state.player.inventory[0].name))
        except IndexError:
            self.state.assistant.say("Your inventory is currently empty!")   
        idling = True
        while (idling):
            playerChoice = self.handlePlayerInput()
            if playerChoice <= 0:
                idling = False
        self.state.assistant.say("Returning!")
        if playerChoice < 0:
            return -1
        else:
            return 0
    
    def handlePlayerInput(self):
        ''' This function handles player input in their inventory '''
        events = get_gamepad()
        for event in events:
            if event.code == "BTN_SOUTH" and event.state == 0:
                try:
                    item = self.state.player.inventory.pop(self.itemIndex)
                    item.use()
                    self.state.assistant.say("Item Used!")
                    self.state.assistant.say("... Well it would have been used, but item effects are not fully implemented yet!")
                except:
                    self.state.assistant.say("You cannot use items you don't have!")
                # TODO DO AN EFFECT
                time.sleep(1)
                try:
                    self.state.assistant.say(self.state.player.inventory[self.itemIndex].name)
                except IndexError:
                    self.state.assistant.say("You have no more items!")
                return -1
            elif event.code == "BTN_EAST" and event.state == 0:
                return 0
            elif event.code == "BTN_NORTH" and event.state == 0:
                self.state.assistant.say(self.state.player.inventory[self.itemIndex].name)
                return 1
        return 1