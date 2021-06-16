class Item():
    def __init__(self, state, id, name, effectID, price):
        self.state = state
        self.id = id
        self.name = name
        self.effectID = effectID
        self.price = price
    
    def use(self):
        self.handle_effect(self.effectID)
    
    def toString(self):
        print(self.id)
        print(self.name)
        print(self.effectID)

    def handle_effect(self, effect_id):
        if str(effect_id) == "1":
            self.state.player.health += 10
        elif str(effect_id) == "2":
            self.state.player.effect_pool = []
        elif str(effect_id) == "3":
            self.state.player.effect_pool.append(["healing", 4])
        elif str(effect_id) == "4":
            self.state.player.effect_pool.append(["strong", 4])
        elif str(effect_id) == "5":
            self.state.player.effect_pool.append(["agile", 4])
        elif str(effect_id) == "6":
            self.state.player.mana += 10
        elif str(effect_id) == "7":
            self.state.player.effect_pool.append(["water", 4])
        elif str(effect_id) == "8":
            self.state.player.effect_pool.append(["fire", 4])
        elif str(effect_id) == "9":
            self.state.player.effect_pool.append(["lightning", 4])
        elif str(effect_id) == "10":
            self.state.player.effect_pool.append(["blocking", 4])
        else:
            print("Item effect ID invalid")

if __name__ == "__main__":
    from StateMachine import StateMachine
    testItem = Item(StateMachine(), 1, "Test Item", 1)