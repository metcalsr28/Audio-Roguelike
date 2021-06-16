import random as rand
import inputs as inp
from BattleState import BattleState
from InventoryState import InventoryState
from inputs import get_gamepad

class RoomState():
    def __init__(self, state):
        self.state = state
        self.loot_queue = []
        self.encounterRate = None
        self.freeItemRate = None

        '''Determine room biome'''
        if self.state.floor_number > 0 and self.state.floor_number < 11:
            self.state.current_biome = self.state.biomes[1]
        elif self.state.floor_number > 10 and self.state.floor_number < 16:
            self.state.current_biome = self.state.biomes[5]
        elif self.state.floor_number == "Leisure Area":
            self.state.current_biome = self.state.biomes[2]
        elif self.state.floor_number == "HR":
            self.state.current_biome = self.state.biomes[4]
        elif self.state.floor_number == "IT":
            self.state.current_biome = self.state.biomes[3]
        else:
            print("Error Occured: floor state unknown. Using 'cubical farm' settings")

        self.state.assistant.say("You enter the next room!")

        '''Determine whether battle will occur. Battle state will handle determining opponent'''
        if self.state.difficulty == "Easy":  # TODO consider difficulty settings
            self.encounterRate = .75
            self.freeItemRate = .25
        if self.state.room_number != 5:
            if rand.randint(1, 100) <= self.encounterRate * 100:
                BattleState(self.state, isBoss=False)
        else:
            BattleState(self.state, isBoss=True)
        
        '''Determine and Inform player of objects in room'''
        if rand.randint(1, 100) <= self.freeItemRate * 100:
            lootIndex = rand.randint(0, len(self.state.items) - 1)
            loot = self.state.items[lootIndex]
            if loot.name[0] == 'A' or loot[0].name == 'U' or loot[0].name == 'E' or loot[0].name == 'I' or loot[0].name == 'O':
                self.state.assistant.say("You see an {} in the room.".format(loot.name))
                self.loot_queue.append(loot)
            else:
                self.state.assistant.say("You see a {} in the room.".format(loot.name))
                self.loot_queue.append(loot)
        
        '''Await player action'''
        idling = True
        while(idling):
            playerChoice = self.handlePlayerInput()
            if playerChoice == -1:
                idling = False
        if self.state.room_number != 5:
            self.state.room_number += 1
        else:
            self.state.room_number = 1
            self.state.floor_number += 1
            
    def handlePlayerInput(self):
        ''' This function handles player input in between room transitions '''
        events = get_gamepad()
        for event in events:
            if event.code == "BTN_SOUTH" and event.state == 0:
                try: 
                    loot = self.state.player.addToInventory(self.loot_queue.pop())
                    self.state.assistant.say("You take the {}".format(loot.name))
                    
                except:
                    return -1
            elif event.code == "BTN_WEST" and event.state == 0:
                InventoryState(self.state)
                return 0
            elif event.code == "BTN_NORTH" and event.state == 0:
                self.state.assistant.explain_surroundings()
                return 1
        return 0


if __name__ == "__main__":
    ''' Running this script as main creates a test room for the player to interact with '''
    from StateMachine import StateMachine
    state = StateMachine()
    testFloor = RoomState(state)



