import time
from inputs import get_gamepad
from Item import Item
class InventoryState:
    def __init__(self, state):
        self.state = state
        self.item_index = 0
        self.start()
    
    def start(self):
        self.state.assistant.say("Inventory!")
        time.sleep(.5)
        try:
            if len(self.state.player.inventory) == 1:
                self.state.assistant.say("You have {} item, starting with {}".format(len(self.state.player.inventory), 
                                                                                    self.state.player.inventory[0].name))
            else:
                self.state.assistant.say("You have {} items, starting with {}".format(len(self.state.player.inventory), 
                                                                                    self.state.player.inventory[0].name))
        except IndexError:
            self.state.assistant.say("Your inventory is currently empty!")   
        idling = True
        while (idling):
            playerChoice = self.handlePlayerInput()
            if playerChoice == -1:
                idling = False
        self.state.assistant.say("Returning!")

    def toggle_selection(self, positive=True):
        if positive:
            self.item_index += 1
            if self.item_index == len(self.state.player.inventory):
                self.item_index = 0
            self.state.assistant.say(self.state.player.inventory[self.item_index].name)
        elif not positive:
            self.item_index -= 1
            if self.item_index < 0:
                self.item_index == len(self.state.player.inventory) - 1
            self.state.assistant.say(self.state.player.inventory[self.item_index].name)  

    def handlePlayerInput(self):
        ''' This function handles player input in their inventory '''
        events = get_gamepad()
        for event in events:
            if event.code == "ABS_X" and event.state > 3000:
                self.toggle_selection(True)
            elif event.code == "ABS_X" and event.state < -3000:
                self.toggle_selection(False)
            elif event.code == "BTN_SOUTH" and event.state == 0:
                try:
                    item = self.state.player.inventory.pop(self.item_index)
                    item.use()
                    self.state.assistant.say("Item Used!")
                except:
                    self.state.assistant.say("You cannot use items you don't have!")
                time.sleep(.5)
                try:
                    self.state.assistant.say(self.state.player.inventory[self.item_index].name)
                except IndexError:
                    self.state.assistant.say("You have no more items!")
                if self.state.in_combat == True:
                    return -1
                else: 
                    return 0
            elif event.code == "BTN_EAST" and event.state == 0:
                return -1
            elif event.code == "BTN_NORTH" and event.state == 0:
                self.state.assistant.say(self.state.player.inventory[self.item_index].name)
                return 0
        return 0