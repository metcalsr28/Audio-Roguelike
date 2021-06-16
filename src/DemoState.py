from StateMachine import StateMachine
from Assistant import Assistant
from inputs import get_gamepad
from TownState import TownState
#from playsound import playsound
from multiprocessing import Process
from threading import Thread
from time import sleep
#import winsound
#import pygame
import simpleaudio as sa
from queue import Queue

def play_music(state):
        wave_obj = sa.WaveObject.from_wave_file("sound effects\\main-theme-50-percent.wav")
        play_obj = wave_obj.play()
        while play_obj.is_playing():
            if q.get() == "stop":
                play_obj.stop()
                print("stop successful")

if __name__ == "__main__":
    state = StateMachine()
    q = Queue()
    wave_obj = Thread(target=play_music, args=(q,))
    wave_obj.start()
    
    sleep(1)
    # state.assistant.say(" Salutations adventurer!\
    # In this game you play the night stalker (name pending) \
    # a blind swordsman who's special powers make him perfectly \
    # suited to slaying the things that go bump in the night!\
    # This demo showcases this projects new emphasis on sound as\
    # a key narrative device.\
    # Along with the change of setting, the game has been modified to\
    # be less linear, using a hub city as a main base of operations \
    # which the player can come back to between outings known as hunts.\
    # Hopefully, this new direction will enable the game to feel more alive \
    # and less repetitive. Go ahead and see for yourself! \
    # You can cycle between areas of the village with the thumbstick,\
    # so feel free to look around!\
    # ")
    state.assistant.say("Welcome to the world of the night stalker!")
    sleep(1)
    state.assistant.say("Press any button to enter the village!")
    ready = False
    while not ready:
        events = get_gamepad()
        for event in events:
            if (event.code == "BTN_SOUTH" or event.code == "BTN_NORTH" or event.code == "BTN_EAST" or event.code == "BTN_WEST") and event.state == 0:
                ready = True
    q.put("stop")
    wave_obj = sa.WaveObject.from_wave_file("sound effects\\running.wav")
    play_obj = wave_obj.play()
    sleep(.25)
    state.assistant.say("You arrive in the town!")
    TownState(state)
    
