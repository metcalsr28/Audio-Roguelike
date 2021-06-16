'''
Author: Steve Metcalf
Title: Audio Roguelike
Description: This project seeks to examine ways in which archetypal video game genres can be made more accessible 
            and is meant to serve as a capstone project for a degree in Information Technology at Miami University

__main__.py:
    This is the main file which will handle execution of the program.
'''
from StateMachine import StateMachine
from Assistant import Assistant

if __name__ == "__main__":
    state = StateMachine()
    nano = Assistant(state)
    nano.changeVoiceGender('female')
    nano.say("Hello, It is nice to meet you. I'm your new personal assistant Nano. I'll be here to help you out during your journey")
    nano.say("For now, we are attached at the hip. Just kidding. I have grafted myself to your arm!")
    nano.say("I am fitted with a bomb that will detonate in approximately, three, hours. Please obtain a registration key before that time.")
    nano.say("Don't worry! You will not die alone. I estimate all life will seize to exist in a 3-block radius!")
    nano.say("I hope I have been able to provide some comfort in your final moments! dot dot dot. Not that these are your final moments!")
    #assistant.say("Don't touch me like that!")
    #assistant.say("it's dangerous to go alone, take this. dot dot dot. A little to your left. There you go!")
    #assistant.say("um")
    #assistant.say("Shake shake shake senora")

    pass
