from audio import Audio
from alarm_set import AlarmSet

class ScreenContext:
    def __init__(self, settings, screen_stack, display):

        self.stack = screen_stack
        self.alarms = AlarmSet(settings)
        self.display = display
        self.audio = Audio(settings)
        self.settings = settings
