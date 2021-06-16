import random as rand
import simpleaudio as sa
class Player:
    def __init__(self, state):
        self.state = state
        self.rank = 1
        self.health = 14
        self.max_health = 11 + (3 * self.rank)
        self.mana = 10
        self.max_mana = 8 + (2 * self.rank)
        self.strength = 5
        self.agility = 5
        self.attack_type = "normal"
        self.abilities = []
        self.isBlocking = False
        self.inventory = []
        self.gold = 50
        self.effect_pool = []
        self.forfeit_turn = False

    def handle_effect_pool(self):
        for x in range(len(self.effect_pool)):
            if self.effect_pool[x][0] == "bleeding":
                wave_obj = sa.WaveObject.from_wave_file("sound effects\\bleed.wav")
                play_obj = wave_obj.play()
                self.health -= 1
            elif self.effect_pool[x][0] == "poisoned":
                wave_obj = sa.WaveObject.from_wave_file("sound effects\\poison.wav")
                play_obj = wave_obj.play()
                self.health -= 1
            elif self.effect_pool[x][0] == "stunned":
                wave_obj = sa.WaveObject.from_wave_file("sound effects\\constricted.wav")
                play_obj = wave_obj.play()
                self.forfeit_turn = True
            elif self.effect_pool[x][0] == "healing":
                wave_obj = sa.WaveObject.from_wave_file("sound effects\\healing.wav")
                play_obj = wave_obj.play()
                self.health += 5
            elif self.effect_pool[x][0] == "strong":
                wave_obj = sa.WaveObject.from_wave_file("sound effects\\grunt.wav")
                play_obj = wave_obj.play()
                self.strength += 5
            elif self.effect_pool[x][0] == "agile":
                wave_obj = sa.WaveObject.from_wave_file("sound effects\\swift.wav")
                play_obj = wave_obj.play()
                self.agility += 5
            elif self.effect_pool[x][0] == "water":
                wave_obj = sa.WaveObject.from_wave_file("sound effects\\water.wav")
                play_obj = wave_obj.play()
                self.attack_type = "water"
            elif self.effect_pool[x][0] == "fire":
                wave_obj = sa.WaveObject.from_wave_file("sound effects\\crackle.wav")
                play_obj = wave_obj.play()
                self.attack_type = "fire"
            elif self.effect_pool[x][0] == "lightning":
                wave_obj = sa.WaveObject.from_wave_file("sound effects\\zap.wav")
                play_obj = wave_obj.play()
                self.attack_type = "lightning"
            elif self.effect_pool[x][0] == "blocking":
                wave_obj = sa.WaveObject.from_wave_file("sound effects\\shielded.wav")
                play_obj = wave_obj.play()
                self.isBlocking = True
            elif self.effect_pool[x][0] == "rank buff":
                self.strength += 5
                self.agility += 5
            else:
                print("Effect pool error")
            self.effect_pool[x][1] -= 1 # reducing duration of effect
            if self.effect_pool[x][1] <= 0: # remove effect when duration finishes
                self.effect_pool.remove(x)
                # handle return of stats to normal values
                if [x][0] == "strong":
                    self.strength -= 5
                elif [x][0] == "agile":
                    self.agility -= 5
                elif [x][0] == "water":
                    self.attack_type = "normal"
                elif [x][0] == "fire":
                    self.attack_type = "normal"
                elif [x][0] == "lightning":
                    self.attack_type = "normal"
                elif [x][0] == "blocking":
                    self.isBlocking = False
                elif [x][0] == "rank buff":
                    self.strength -= 5
                    self.agility -= 5

    def attack(self, enemy):
        accuracyRoll = rand.randint(self.agility, 10 + self.agility)
        dodgeRoll = rand.randint(enemy.agility, 10 + enemy.agility)
        if accuracyRoll > dodgeRoll:
            attackDamage = rand.randint(1, self.strength)
            if self.attack_type != "normal":
                damage_multiplier = self.check_enemy_weakness(enemy.get_affinity())
                attackDamage *= damage_multiplier
                if self.attack_type == "water":
                    wave_obj = sa.WaveObject.from_wave_file("sound effects\\water_attack.wav")
                    play_obj = wave_obj.play()
                elif self.attack_type == "fire":
                    wave_obj = sa.WaveObject.from_wave_file("sound effects\\fire_attack.wav")
                    play_obj = wave_obj.play()
                elif self.attack_type == "lightning":
                    wave_obj = sa.WaveObject.from_wave_file("sound effects\\lightning_attack.wav")
                    play_obj = wave_obj.play()
                else:
                    print("Problem parsing attack type")
            else:    
                wave_obj = sa.WaveObject.from_wave_file("sound effects\\oof.wav")
                play_obj = wave_obj.play()
            enemy.health -= attackDamage
        else:
            wave_obj = sa.WaveObject.from_wave_file("sound effects\\whiff.wav")
            play_obj = wave_obj.play()
    
    def check_enemy_weakness(self, enemy_affinity):
        if self.attack_type == "water":
            if enemy_affinity == "fire":
                return 2.0
            elif enemy_affinity == "lightning":
                return .5
        elif self.attack_type == "fire":
            if enemy_affinity == "lightning":
                return 2.0
            elif enemy_affinity == "water":
                return .5
        if self.attack_type == "lightning":
            if enemy_affinity == "water":
                return 2.0
            elif enemy_affinity == "fire":
                return .5
    
    def addToInventory(self, item):
        self.inventory.append(item)
    
    def rank_up(self):
        self.max_health += (3 * self.rank)
        self.health = self.max_health
        self.max_mana += (2 * self.rank)
        self.mana = self.max_mana
        self.strength += 1
        self.agility += 1
        self.rank += 1