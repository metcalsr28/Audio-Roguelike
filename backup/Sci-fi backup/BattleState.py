import random as rand
from inputs import get_gamepad
from InventoryState import InventoryState
from Monster import Monster
class BattleState():
    def __init__(self, state, isBoss=False):
        self.state = state
        self.isBoss = isBoss
        self.handle_combat()

    def handle_combat(self):
        ''' 
        Combat involves a setup phase, followed by a series of three step 'rounds.' 
        Combat ends when player or monster are incapacitated a reward is given.
        Setup phase: Determines opponent and turn order
        Stage 1: Monster or player takes turn depending on turn order.
        Stage 2: other party takes turn
        Stage 3: Check if battle has ended.
        '''
        opponent = self.determine_opponent()
        self.state.assistant.announce_opponent(opponent)
        playersTurn = self.determine_turn_order(opponent)
        if playersTurn:
            self.state.assistant.say("You gain the initiative!")
        battleOngoing = True
        while battleOngoing:
            if playersTurn:
                while playersTurn > 0:
                    playersTurn = self.handlePlayerInput(opponent)
            else:
                opponent.attack(self.state.player)
                playersTurn = 1
            print(opponent.health)
            if opponent.health <= 0:
                battleOngoing = False
        self.determine_reward(opponent)


    def determine_opponent(self):
        ''' 
        Based on the current biome, determine a suitable opponent.
        '''
        if not self.isBoss:
            encounterableEnemies = self.state.encounterable_enemies[self.state.current_biome[0]]
            print(encounterableEnemies)
            enemyIndex = rand.randint(0, len(encounterableEnemies) - 1)
            encountered = encounterableEnemies[enemyIndex]
            for enemy in self.state.enemies:
                if enemy.name == encountered:
                    opponent = enemy
            return opponent
        else:
            opponent = self.state.current_biome["bosses"][0]
            return opponent

    def determine_turn_order(self, opponent):
        ''' 
        Determines who initiates combat
        return true if player starts first 
        ''' 
        return self.state.player.dodge_chance > int(opponent.dodge_chance)

    def determine_reward(self, opponent):
        '''
        Determines appropriate reward based on opponent type
        '''
        if not self.isBoss:
            opponent.drop_loot()
        else:
            reward = self.state.current_biome["Unique Rewards"]
            self.state.player.addToInventory(reward)
            if reward[0] == 'A' or reward[0] == 'U' or reward[0] == 'E' or reward[0] == 'I' or reward[0] == 'O':
                self.state.assistant.say("You received an {}".format(reward))
            else:
                self.state.assistant.say("You received a {}".format(reward))

    def handlePlayerInput(self, opponent):
        ''' This function handles player input in between room transitions '''
        events = get_gamepad()
        for event in events:
            if event.code == "BTN_SOUTH" and event.state == 0:
                self.state.player.attack(opponent)
                if opponent.health <= 0:
                    return -1
                else: 
                    return 0
            elif event.code == "BTN_WEST" and event.state == 0:
                ''' 
                Lets the player access inventory,will end turn if player uses 
                an item
                '''
                inv = InventoryState(self.state)
                usedItem = inv.start()
                return usedItem
            elif event.code == "BTN_NORTH" and event.state == 0:
                self.state.assistant.explain_battle(opponent)
                return 1
        return 1

if __name__ == "__main__":
    ''' If this script is ran as main, it will demonstrate a mock battle.'''
    # Determine opponent

    # Compare statistics of player and opponent

    # Handle combat

    # Determine reward, if any.

    # Exit Battle State
