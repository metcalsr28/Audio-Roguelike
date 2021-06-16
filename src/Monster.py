import random as rand
import simpleaudio as sa
from abilities import perform_ability

class Monster():
    def __init__(self, state, mon_type):
        self.state = state
        '''bringing in monster data'''
        self.name = mon_type[0]
        self.cost = int(mon_type[1])
        self._affinity = mon_type[2]
        self._stat_modifier = mon_type[3]
        self.cool_down = int(mon_type[4])
        self._on_cool_down = False
        self._time_on_cool_down = 0
        self._abilities = mon_type[5:]

        '''Instantiating stat sheet'''
        self.strength = 0
        self.agility = 0
        self.health = 0   
        
        '''preapplying modifiers'''
        if self._stat_modifier == "fast":
            self.agility += 2
        elif self._stat_modifier == "sturdy":
            self.health += 2
        elif self._stat_modifier == "strong":
            self.strength += 2
            self.health += 2

        '''Scaling with cost'''
        self.strength += self.cost * 2
        self.agility += self.cost * 2
        self.health += self.cost * 2

    def battle_cry(self):
        wave_obj = sa.WaveObject.from_wave_file("sound effects\\monster sounds\\" + self.name + "_cry.wav")
        play_obj = wave_obj.play()

    def attack(self, enemy):
        self.battle_cry()
        if not self._on_cool_down:
            self.do_special_ability(enemy)
        else:
            self._time_on_cool_down += 1
            accuracyRoll = rand.randint(self.agility, 10 + self.agility)
            dodgeRoll = rand.randint(enemy.agility, 10 + enemy.agility)
            if accuracyRoll > dodgeRoll:
                attackDamage = rand.randint(1, self.strength)
                # self.state.assistant.say("They attack and deal {} damage!".format(attackDamage))
                wave_obj = sa.WaveObject.from_wave_file("sound effects\\oof.wav")
                play_obj = wave_obj.play()
                enemy.health -= attackDamage
            else:
                wave_obj = sa.WaveObject.from_wave_file("sound effects\\whiff.wav")
                play_obj = wave_obj.play()
        if self._time_on_cool_down == self.cool_down:
            self._on_cool_down = False
            self._time_on_cool_down = 0

    def do_special_ability(self, enemy):
        ability_preference = .5 # percentage likelihood of ability usage
        for x in range(len(self._abilities)):
            if ability_preference - rand.random():
                self._on_cool_down = True
                perform_ability(self, enemy,ability=self._abilities[x])
            self._on_cool_down = True

    