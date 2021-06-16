import random as rand
class Player:
    def __init__(self, state):
        self.state = state
        self.health = 8
        self.level = 1
        self.attack_power = 3
        self.accuracy = 3
        self.dodge_chance = 3
        self.inventory = []
    
    def attack(self, enemy):
        accuracyRoll = rand.randint(self.accuracy, 10 + self.accuracy)
        dodgeRoll = rand.randint(enemy.dodge_chance, 10 + enemy.dodge_chance)
        if accuracyRoll > dodgeRoll:
            attackDamage = rand.randint(1, self.attack_power)
            self.state.assistant.say("You deal {} damage!".format(attackDamage))
            enemy.health -= attackDamage
        else:
            self.state.assistant.say("They dodged!")
    
    def addToInventory(self, item):
        self.inventory.append(item)
    