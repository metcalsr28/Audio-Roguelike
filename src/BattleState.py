import random as rand
from inputs import get_gamepad
from InventoryState import InventoryState
from Monster import Monster
import time
import simpleaudio as sa
import copy

class BattleState:
    def __init__(self, state, GT=False, isBoss=False):
        self.state = state
        self.isBoss = isBoss
        self.monster_index = 0
        if GT:
            self.state.gt_difficulty = self.state.gt_floor_number * 2
            self.difficulty = self.state.gt_difficulty
        else:
            self.difficulty = self.state.difficulty
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
        self.state.assistant.say("You've entered combat")
        self.state.in_combat = True
        print("determining opponents")
        opponentList = self.determine_opponents()
        print("opponents determined")
        print("opponents: ")
        for x in range(len(opponentList)): 
            print(opponentList[x].name)
        for opponent in opponentList:
            opponent.battle_cry()
            time.sleep(1)
        playersTurn = self.determine_turn_order(opponentList)
        if playersTurn:
            self.state.assistant.say("You gain the initiative!")
        battleOngoing = True
        while battleOngoing:
            # turn setup
            for opponent in opponentList:
                print(opponent.name + ": " + str(opponent.health))
                if opponent.health <= 0:
                    opponentList.remove(opponent)
                    self.monster_index -= 1
                    if self.monster_index < 0:
                        self.monster_index = len(opponentList) - 1
            
            # turn handling
            if playersTurn >= 0: # TODO MAKE THIS LINE NOT HIDEOUS, EVEN IT'S NOT THE PROBLEM
                if self.state.player.health <= 0:
                    battleOngoing = False
                    gameOver = True
                    self.state.in_combat = False
                    return gameOver
                self.state.player.handle_effect_pool()
                if self.state.player.forfeit_turn:
                    playersTurn = -1
                    continue
                while not playersTurn -1:
                    playersTurn = self.handlePlayerInput(opponentList)
            else:
                for x in range(len(opponentList)):
                    opponentList[x].attack(self.state.player)
                playersTurn = 1
            if opponentList == []:
                battleOngoing = False
                print("battle over")
                continue
            time.sleep(2)
        self.state.in_combat = False

    def determine_opponents(self):
        ''' 
        Determines a suitable list of opponents.
        '''
        print(self.difficulty)
        if not self.isBoss:
            cost_consumed = 0
            enemyList = []
            while cost_consumed == 0:
                enemyList = []
                while cost_consumed <= self.difficulty / 1.5 and len(enemyList) < 3:
                    next_enemy = self.state.enemies[rand.randint(0, len(self.state.enemies) - 1)]
                    print(next_enemy.name)
                    if next_enemy.cost > self.difficulty: # removes monsters that are too high
                        continue
                    print(next_enemy.cost)
                    print(self.difficulty / 4)
                    if next_enemy.cost >= self.difficulty / 4: # don't want enemies to show up too weak
                        if next_enemy.cost <= self.difficulty - cost_consumed:
                            enemyList.append(next_enemy)
                            cost_consumed += next_enemy.cost
                if enemyList == [] or cost_consumed < self.difficulty / 2:
                    cost_consumed = 0
            copyList = []
            for x in enemyList:
                copyList.append(copy.copy(x)) # This ensures exist as separate enities during combat.
            return copyList
        else:
            opponent = self.state.bosses(self.state.boss_index)
            return opponent

    def determine_turn_order(self, opponentList):
        ''' 
        Determines who initiates combat
        return true if player starts first 
        ''' 
        playersTurn = 1
        for opponent in opponentList:
            if opponent.agility > self.state.player.agility:
                playersTurn = -1
        return playersTurn

    # def determine_reward(self, opponent):
    #     '''
    #     Determines appropriate reward based on opponent type
    #     '''
    #     if not self.isBoss:
    #         opponent.drop_loot()
    #     else:
    #         reward = self.state.current_biome["Unique Rewards"]
    #         self.state.player.addToInventory(reward)
    #         if reward[0] == 'A' or reward[0] == 'U' or reward[0] == 'E' or reward[0] == 'I' or reward[0] == 'O':
    #             self.state.assistant.say("You received an {}".format(reward))
    #         else:
    #             self.state.assistant.say("You received a {}".format(reward))

    def determine_escrow(self):
        self.state.escrow += 1.5 * self.difficulty

    def handlePlayerInput(self, opponentList):
        ''' This function handles player input in between room transitions '''
        events = get_gamepad()
        for event in events:
            if event.code == "ABS_X" and event.state > 3000:
                wave_obj = sa.WaveObject.from_wave_file("sound effects\\tink.wav")
                play_obj = wave_obj.play()
                self.monster_index += 1
                if self.monster_index == len(opponentList):
                    self.monster_index = 0
                time.sleep(.25)
                opponentList[self.monster_index].battle_cry()
                time.sleep(.25)
            elif event.code == "ABS_X" and event.state < -3000:
                wave_obj = sa.WaveObject.from_wave_file("sound effects\\tink.wav")
                play_obj = wave_obj.play()
                self.monster_index -= 1
                if self.monster_index < 0:
                    self.monster_index = len(opponentList) - 1
                time.sleep(.25)
                opponentList[self.monster_index].battle_cry()
                time.sleep(.25)
            elif event.code == "BTN_SOUTH" and event.state == 0:
                self.state.player.attack(opponentList[self.monster_index])
                return -1
            elif event.code == "BTN_WEST" and event.state == 0:
                ''' 
                Lets the player access inventory, will end turn if player uses
                an item
                '''
                inv = InventoryState(self.state)
                usedItem = inv.start()
                return usedItem
            elif event.code == "BTN_NORTH" and event.state == 0:
                self.state.assistant.explain_battle(opponentList[self.monster_index])
                return 0
        return 0

if __name__ == "__main__":
    from StateMachine import StateMachine
    ''' If this script is ran as main, it will demonstrate a mock battle.'''
    state = StateMachine()
    state.gt_floor_number = 20
    battleState = BattleState(state, GT=True, isBoss=False)
