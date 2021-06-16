import pyttsx3

class Assistant:
    def __init__(self, state):
        self.engine = pyttsx3.init()
        self.state = state
        self.changeVoiceGender("Female")

    def say(self, text):
        self.engine.setProperty('rate', 150)
        self.engine.say(text)
        self.engine.runAndWait()

    def explain_surroundings(self):
        self.say("You are in room {} of floor {}.".format(self.state.room_number, self.state.floor_number))
        self.say("You have {} health remaining.".format(self.state.player.health))
    
    def announce_opponent(self, opponent):
        if opponent.name[0] == 'A' or opponent.name[0] == 'U' or opponent.name[0] == 'E' or opponent.name[0] == 'I' or opponent.name[0] == 'O':
            self.state.assistant.say("An {} attacks!".format(opponent.name))
        else:
            self.state.assistant.say("A {} attacks!".format(opponent.name))

    def explain_battle(self, opponent):
        self.say("Enemy Health: {}".format(opponent.health))
        self.say("You have {} health remaining.".format(self.state.player.health))

    def changeVoiceGender(self, gender):   
        voices = self.engine.getProperty('voices')
        if gender == "male":
            self.engine.setProperty('rate', 100)
            self.engine.setProperty('voice', voices[0].id)
        else:
            self.engine.setProperty('rate', 125)
            self.engine.setProperty('voice', voices[1].id)