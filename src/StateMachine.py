import json
from Assistant import Assistant
from Player import Player
from Item import Item
from Monster import Monster
from Spell import Spell

class StateMachine():
    def __init__(self):
        ''' STATE VARIABLES '''
        self.assistant = Assistant(self)
        self.player = Player(self)
        self.difficulty = 3
        self.stop_playing_trigger = False
        self.in_combat = False
        self.on_hunt = False
        self.room_number = 1
        self.gt_encounter_number = 0
        self.gt_floor_number = 1
        self.gt_difficulty = 0
        self.floor_number = 1
        self.town_areas = []
        self.area_descriptors = []
        self.enemies = []
        self.bosses = []
        self.items = []
        self.spells = []
        ''' reading in information from tables '''
        with open('town_areas.csv') as F:
            areasList = F.readlines()
            for x in range(len(areasList)):
                self.town_areas.append(areasList[x].strip('\n').split(','))
        with open('monsters.csv') as F:
            enemiesList = F.readlines()
            for x in range(1, len(enemiesList)):
                enemy = Monster(self, enemiesList[x].strip('\n').split(','))
                self.enemies.append(enemy)
        with open('bosses.csv') as F:
            bossList = F.readlines()
            for x in range(1, len(bossList)):
                enemy = Monster(self, bossList[x].strip('\n').split(','))
                self.bosses.append(enemy)
        with open('items.csv') as F:
            itemsList = F.readlines()
            for x in range(1,len(itemsList)):
                itemInfo = itemsList[x].strip('\n').split(',')
                self.items.append(Item(self, itemInfo[0], itemInfo[1], itemInfo[2], itemInfo[3]))
        with open('spells.csv') as F:
            spellList = F.readlines()
            for x in range(1,len(spellList)):
                spellInfo = spellList[x].strip('\n').split(',')
                self.spells.append(Spell(self, spellInfo[0], spellInfo[1], spellInfo[2], spellInfo[3]))

        '''adding a more direct reference to the area descriptors'''
        for x in range(len(self.town_areas)):
            self.area_descriptors.append(self.town_areas[x][2])

if __name__ == "__main__":
    state = StateMachine()
    print("Town Areas:")
    print(state.areas)
    print("\n\n")
    print("Enemies:")
    print(state.enemies)
    print("\n\n")
    print("Bosses:")
    print(state.bosses)
    print("\n\n")
    print("Items:")
    print(state.items)
    print("\n\n")
    print("spells:")
    print(state.spells)