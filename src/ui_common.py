class Event:
    # Handled by event manager
    SHUTDOWN = -1000

    # Recieved in current screen
    ENTER = 0
    EXIT = 1
    POLL = 2
    BUTTON_DOWN = 3 
    BUTTON_UP = 4

    @staticmethod
    def user_event(event):
        return event == Event.BUTTON_DOWN or event == Event.BUTTON_UP

    @staticmethod
    def button_event(event):
        return event == Event.BUTTON_DOWN or event == Event.BUTTON_UP

class Button:
    OK = 0
    CANCEL = 3
    LEFT = 1
    RIGHT = 2
