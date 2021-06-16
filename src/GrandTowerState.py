import random as rand
import inputs as inp
from BattleState import BattleState
import time
import simpleaudio as sa
from inputs import get_gamepad
from InventoryState import InventoryState

class GrandTowerState():
    def __init__(self, state):
        self.state = state
        self.loot_queue = []
        self.encounter_number = self.state.gt_encounter_number = 0
        self.floor_number = self.state.gt_floor_number
        self.state.assistant.say("You leave the town!")
        self.game_over = False

        '''Determine whether battle will occur. Battle state will handle determining opponent'''
        while self.encounter_number < 10 and not self.game_over:
            print("Got through battle setup!")
            self.game_over = BattleState(self.state, GT=True, isBoss=False)
            self.encounter_number += 1
            if self.game_over:
                self.state.assistant.say("You're gravely wounded. You abandon the mission. You return town.")
                self.state.player.health = 1
                self.state.player.effect_pool = []
                self.state.escrow = 0
        if not self.game_over:
            print("Got through battle setup!")
            self.state.gt_floor_number += 1
            if not self.state.gt_floor_number % 5:
                self.game_over = BattleState(self.state, GT=True, isBoss=True)
                if self.game_over:
                    self.state.assistant.say("You're gravely wounded. You abandon the mission. You return town.")
                    self.state.player.health = 1
                    self.state.player.effect_pool = []
                    self.state.escrow = 0
        self.state.assistant.say("You return to town. You sell the goods from the expedition for " + str(self.state.escrow) + " gold pieces!")
        self.state.player.gold += self.state.escrow
        self.state.escrow = 0
        
        # '''Determine and Inform player of objects in room'''
        # if rand.randint(1, 100) <= self.freeItemRate * 100:
        #     lootIndex = rand.randint(0, len(self.state.items) - 1)
        #     loot = self.state.items[lootIndex]
        #     if loot.name[0] == 'A' or loot[0].name == 'U' or loot[0].name == 'E' or loot[0].name == 'I' or loot[0].name == 'O':
        #         self.state.assistant.say("You see an {} in the room.".format(loot.name))
        #         self.loot_queue.append(loot)
        #     else:
        #         self.state.assistant.say("You see a {} in the room.".format(loot.name))
        #         self.loot_queue.append(loot)
        
        # '''Await player action'''
        # idling = True
        # playerChoice = 0
        # while(idling):
        #     playerChoice = self.handlePlayerInput()
        #     if playerChoice == -1:
        #         idling = False
        # if self.state.room_number != 5:
        #     self.state.room_number += 1
        # else:
        #     self.state.room_number = 1
        #     self.state.floor_number += 1
            
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



