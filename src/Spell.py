class Spell():
    def __init__(self, state, id, name, mana_cost, price):
        self.state = state
        self.id = id
        self.name = name
        self.mana_cost = mana_cost
        self.price = price
    
    def use(self, enemy=None):
        self.handle_effect(self.name, enemy)
    
    def toString(self):
        print(self.id)
        print(self.name)
        print(self.mana_cost)

    def handle_effect(self, enemy=None):
        if self.mana_cost > self.state.player.mana:
            castable = False
            return castable
        self.state.player.mana -= self.mana_cost
        if self.name == "Fire Bolt":
            self.state.player.deal_spell_damage("fire", 6 + self.state.player.rank)
        elif self.name == "Lightning Touch":
            self.state.player.deal_spell_damage("lightning", 6 + self.state.player.rank)
        elif self.name == "Mist Spray":
            self.state.player.deal_spell_damage("water", 6 + self.state.player.rank)
        elif self.name == "Iron Skin":
            self.state.player.effect_pool.append(["blocking", 4])
        elif self.name == "Adrenaline Rush":
            self.state.player.effect_pool.append(["strong", 4])
        elif self.name == "Super Speed":
            self.state.player.effect_pool.append(["agile", 4])
        else:
            print("Spell name invalid")

if __name__ == "__main__":
    from StateMachine import StateMachine
    testItem = Item(StateMachine(), 1, "Test Item", 1)