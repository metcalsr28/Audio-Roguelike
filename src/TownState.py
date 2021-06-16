from threading import Thread
from inputs import get_gamepad
import simpleaudio as sa
from queue import Queue
import time
from InventoryState import InventoryState
from HuntState import HuntState
from TavernState import TavernState
from AlchemistState import AlchemistState
from OutskirtsState import OutskirtsState
from TempleState import TempleState
import sys

class TownState():
    def __init__(self, state):
        self.state = state
        self.choice_index = 0
        self.bgm_q = Queue()
        self.bgm_thread = Thread(target=self.play_music, args=(self.bgm_q, "sound effects\\town_theme_quiet.wav", True))
        self.bgm_thread.start()
        self.state.assistant.say("You stand before the local tavern, cheers and merriment can be heard coming from inside!")
        self.am_q = Queue()
        self.music_thread = Thread(target=self.play_music, args=(self.am_q, "sound effects\\" + self.state.town_areas[self.choice_index][1], True))
        self.music_thread.start()
        time.sleep(.5)

        '''Await player action'''
        idling = True
        playerChoice = 0
        while(idling):
            playerChoice = self.handlePlayerInput()
            if playerChoice == -1:
                idling = False
                try:
                    self.bgm_q.put("stop")
                except Exception as e:
                    print(e)
                    pass
                try:
                    self.am_q.put("stop")
                except Exception as e:
                    print(e)
                    pass

    def play_music(self, q, file_name, repeat=False):
        while not q.empty():
            q.get()
        if repeat:
            try:
                done = False
                while not done:
                    wave_obj = sa.WaveObject.from_wave_file(file_name)
                    play_obj = wave_obj.play()
                    while play_obj.is_playing():
                        if not q.empty():
                            if q.get() == "stop":
                                done = True
                                play_obj.stop()
                                time.sleep(1)
                                print("Stopped Sucessfully")
            except Exception as e:
                print(e)
        else:
            try:
                wave_obj = sa.WaveObject.from_wave_file(file_name)
                play_obj = wave_obj.play()
                while play_obj.is_playing():
                    if not q.empty():
                        if q.get() == "stop":
                            play_obj.stop()
                            time.sleep(1)
                            print("Stopped Sucessfully")
            except Exception as e:
                print(e)

    def toggle_selection(self, positive):
        if positive:
            self.choice_index += 1
        else:
            self.choice_index -= 1
        if self.choice_index > len(self.state.town_areas) - 1:
            self.choice_index = 0
        elif self.choice_index < 0:
            self.choice_index = len(self.state.town_areas) - 1
        if self.music_thread is not None:
            try:
                self.am_q.put("stop")
            except Exception as e:
                print(e)
        wave_obj = sa.WaveObject.from_wave_file("sound effects\\running.wav")
        play_obj = wave_obj.play()
        time.sleep(1.5)
        self.music_thread = Thread(target=self.play_music, args=(self.am_q, "sound effects\\" + self.state.town_areas[self.choice_index][1], True))
        self.music_thread.start()

    def handlePlayerInput(self):
        ''' This function handles player input in between room transitions '''
        events = get_gamepad()
        for event in events:
            if event.code == "ABS_X" and event.state > 3000:
                self.toggle_selection(True)
            elif event.code == "ABS_X" and event.state < -3000:
                self.toggle_selection(False)
            elif event.code == "BTN_SOUTH" and event.state == 0:
                try:
                    try:
                        self.bgm_q.put("stop")
                    except Exception as e:
                        print(e)
                        pass
                    try:
                        self.am_q.put("stop")
                    except Exception as e:
                        print(e)
                        pass
                    # play footsteps
                    wave_obj = Thread(target=self.play_music, args=(self.am_q,"sound effects\\running.wav"))
                    wave_obj.start()
                    time.sleep(1.5)
                    if self.choice_index == 0:
                        TavernState(self.state)
                    elif self.choice_index == 1:
                        AlchemistState(self.state)
                    elif self.choice_index == 2:
                        OutskirtsState(self.state)
                    elif self.choice_index == 3:
                        TempleState(self.state)
                    else:
                        raise AssertionError
                except:
                    print("could not parse choice")
                self.state.assistant.say("You return to the town square.")
                '''Reinstantiating town logic'''
                self.bgm_thread = Thread(target=self.play_music, args=(self.bgm_q, "sound effects\\town_theme_quiet.wav", True))
                self.bgm_thread.start()
                time.sleep(2)
                self.music_thread = Thread(target=self.play_music, args=(self.am_q, "sound effects\\" + self.state.town_areas[self.choice_index][1], True))
                self.music_thread.start()
                time.sleep(.5)
            elif event.code == "BTN_WEST" and event.state == 0:
                InventoryState(self.state)
                return 0
            elif event.code == "BTN_NORTH" and event.state == 0:
                self.state.assistant.read_town_area_descriptor(self.choice_index)
                return 0
            elif event.code == "BTN_EAST" and event.state == 0:
                return -1
        return 0

if __name__ == "__main__":
    ''' Running this script as main creates a test room for the player to interact with '''
    from StateMachine import StateMachine
    state = StateMachine()
    state.player.gold = 1000
    testFloor = TownState(state)