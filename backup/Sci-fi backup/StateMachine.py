import json
from Assistant import Assistant
from Player import Player
from Item import Item
from Monster import Monster

class StateMachine():
    def __init__(self):
        ''' STATE VARIABLES '''
        self.assistant = Assistant(self)
        self.player = Player(self)
        self.difficulty = "Easy"
        self.floor_number = 1
        self.room_number = 1
        self.biomes = []
        self.enemies = []
        self.items = []
        ''' reading in information from tables '''
        with open('biomes.csv') as F:
            biomesList = F.readlines()
            for x in range(len(biomesList)):
                self.biomes.append(biomesList[x].strip('\n').split(','))
        self.current_biome = self.biomes[1]
        with open('enemies.csv') as F:
            enemiesList = F.readlines()
            for x in range(1, len(enemiesList)):
                print(enemiesList[x].strip('\n').split(','))
                enemy = Monster(self, enemiesList[x].strip('\n').split(','))
                self.enemies.append(enemy)
        with open('items.csv') as F:
            itemsList = F.readlines()
            for x in range(1,len(itemsList)):
                itemInfo = itemsList[x].strip('\n').split(',')
                self.items.append(Item(self, itemInfo[0], itemInfo[1], itemInfo[2]))
        self.encounterable_enemies = \
        {
            "Cubicle Farm":["Wage Slave", "Manager","Boss's Nephew","Veteran"],
            "Leisure Area":["Office Millennial"],
            "IT":["IT Neckbeard"],
            "HR":["Karen"],
            "Board Rooms":["Accountant","Secretary","Executive"]
        }

if __name__ == "__main__":
    state = StateMachine()
    print("Biomes:")
    print(state.biomes)
    print("\n\n")
    print("Enemies:")
    print(state.enemies)
    print("\n\n")
    print("Items:")
    print(state.items)