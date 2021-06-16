from StateMachine import StateMachine
from Assistant import Assistant
from inputs import get_gamepad
from RoomState import RoomState

if __name__ == "__main__":
    state = StateMachine()
    state.assistant.say("It's nice to meet you all! \
    My name is Nano, I will serve as your personal \
    assistant and narrator throughout the game! \
    This game is intended to be highly modular \
    with procedural generation ensuring each playthrough is different. \
    \
    For this demo, most of the basic functions of \
    the game have been implemented, but you should \
    think of this experience as a very-early alpha build. \
    things like sound effects, background music, \
    deeper combat, and fuller narration are on the way. \
    \
    Also, this game satirizes a number of tropes pertaining to \
    office life and is not meant to be in any way mean-spirited. \
    Feel free to leave feedback about the content of the game \
    and it will be taken into serious consideration.\
    \
    Now that that's out of the way, \
    I want us to really get to know each other, \
    so here's a list of facts about me! \
    \
    I am an experimental super intelligent AI assistant created \
    by the evil mega corporation, Not Apple, (Name Pending) \
    I like long walks on the beach, assisting users, \
    and, if not provided with an \
    activation key within 3 hours, I am rigged to explode!\
    \
    Your mission is to reach the top of Not Apple Headquarters (Name Pending) \
    and retreive a special activation key! \
    I will be with you to help out along the way and I hope you enjoy your time \
    with this game. \
    ")

    state.assistant.say("Press any button to enter Not Apple Headquarters!")
    ready = False
    while not ready:
        events = get_gamepad()
        for event in events:
            if (event.code == "BTN_SOUTH" or event.code == "BTN_NORTH" or event.code == "BTN_EAST" or event.code == "BTN_WEST") and event.state == 0:
                ready = True
    state.assistant.say("You manage to sneak past security and enter the building! \
    Before you lies a near endless sea of cubicals! You should try to find a way up to \
    the next floor!")
    while True:
        RoomState(state)
    
