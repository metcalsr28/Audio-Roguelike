import random as rand
class Monster:
    def __init__(self, state, mon_type):
        self.state = state
        self.name = mon_type[0]
        self.health = int(mon_type[1])
        self.level = int(mon_type[2])
        self.attack_power = int(mon_type[3])
        self.accuracy = int(mon_type[4])
        self.dodge_chance = int(mon_type[5])
        self.drop_table = list(mon_type[6])
    
    def attack(self, enemy):
        accuracyRoll = rand.randint(self.accuracy, 10 + self.accuracy)
        dodgeRoll = rand.randint(enemy.dodge_chance, 10 + enemy.dodge_chance)
        if accuracyRoll > dodgeRoll:
            attackDamage = rand.randint(1, self.attack_power)
            self.state.assistant.say("They attack and deal {} damage!".format(attackDamage))
            enemy.health -= attackDamage
        else:
            self.state.assistant.say("You dodged!")
    def drop_loot(self):
        ''' 
        Iterates through loot table and randomly drops items based their drop chance
        '''
        # for x in self.drop_table:
        #     if rand.randint(0, 100) < x.drop_chance:
        #         self.state.player.addToInventory(x)
        #         if x[0] == 'A' or x[0] == 'U' or x[0] == 'E' or x[0] == 'I' or x[0] == 'O':
        #             self.state.assistant.say("You received an {}".format(x))
        #         else:
        #             self.state.assistant.say("You received a {}".format(x))
    