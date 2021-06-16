class Item():
    def __init__(self, state, id, name, effectID):
        self.state = state
        self.id = id
        self.name = name
        self.effectID = effectID
    def use(self, state):
        self.state.EffectHandler.Do(state, self.effectID)
    def toString(self):
        print(self.id)
        print(self.name)
        print(self.effectID)

if __name__ == "__main__":
    from StateMachine import StateMachine
    testItem = Item(StateMachine(), 1, "Test Item", 1)