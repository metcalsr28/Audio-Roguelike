'''
Name: Abilities.py
Description: file containing the logic for the abilities in the game,
            may at some point consider a better way of doing this,
            but should work for right now.
'''
import random as rand
import simpleaudio as sa


def perform_ability(fighter, enemy, ability="bite"):
    if ability == "bite":
        attackDamage = fighter.strength
        wave_obj = sa.WaveObject.from_wave_file("sound effects\\bite.wav")
        play_obj = wave_obj.play()
        enemy.health -= attackDamage
    elif ability == "slash":
        attackDamage = fighter.strength / 2
        wave_obj = sa.WaveObject.from_wave_file("sound effects\\slash.wav")
        play_obj = wave_obj.play()
        enemy.health -= attackDamage
        bleed_chance = .5
        if bleed_chance - rand.random():
            fighter.state.assistant.say("You're bleeding.")
            enemy.effect_pool.append(["bleeding", 5])
            wave_obj = sa.WaveObject.from_wave_file("sound effects\\bleed.wav")
            play_obj = wave_obj.play()
    elif ability == "poison":
        poison_chance = .80
        if poison_chance - rand.random():
            fighter.state.assistant.say("You've been poisoned.")
            enemy.effect_pool.append(["poisoned", 5])
            wave_obj = sa.WaveObject.from_wave_file("sound effects\\poison.wav")
            play_obj = wave_obj.play()
    elif ability == "shriek":
        shriek_chance = .75
        wave_obj = sa.WaveObject.from_wave_file("sound effects\\shriek.wav")
        play_obj = wave_obj.play()
        if shriek_chance - rand.random():
            enemy.effect_pool.append(["stunned", 2])
            wave_obj = sa.WaveObject.from_wave_file("sound effects\\stun.wav")
            play_obj = wave_obj.play()
    elif ability == "stun":
        stun_chance = .75
        if stun_chance - rand.random():
            enemy.effect_pool.append(["stunned", 3])
            wave_obj = sa.WaveObject.from_wave_file("sound effects\\stun.wav")
            play_obj = wave_obj.play()
    elif ability == "smash":
        attackDamage = fighter.strength
        wave_obj = sa.WaveObject.from_wave_file("sound effects\\bite.wav")
        play_obj = wave_obj.play()
        enemy.health -= attackDamage
        stun_chance = .50
        if stun_chance - rand.random():
            enemy.effect_pool.append(["stunned", 3])
            wave_obj = sa.WaveObject.from_wave_file("sound effects\\smash.wav")
            play_obj = wave_obj.play()
    elif ability == "regenerate":
        fighter.health += 3
        standardAttack(fighter, enemy)

def standardAttack(combat_character, enemy):
    '''
    This function features most of the same logic from a normal attack,
    but does not trigger special attacks and is used for when an ability
    should trigger a normal attack as well
    '''
    accuracyRoll = rand.randint(combat_character.agility, 10 + combat_character.agility)
    dodgeRoll = rand.randint(enemy.agility, 10 + enemy.agility)
    if accuracyRoll > dodgeRoll:
        attackDamage = rand.randint(1, combat_character.strength)
        # fighter.state.assistant.say("They attack and deal {} damage!".format(attackDamage))
        wave_obj = sa.WaveObject.from_wave_file("sound effects\\oof.wav")
        play_obj = wave_obj.play()
        enemy.health -= attackDamage
    else:
        wave_obj = sa.WaveObject.from_wave_file("sound effects\\whiff.wav")
        play_obj = wave_obj.play()