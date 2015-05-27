import time
from datetime import datetime
from event_timer import EventTimer
from ui_common import Button
from ui_framework import LabelWidget
from basic_screen import BasicScreen

_ALARM_LABEL = "-  ALARM  "

def _time_text():
    return datetime.strftime(datetime.now(), "%H:%M")

class AlarmScreen(BasicScreen):
    def __init__(self, context):
        super(AlarmScreen, self).__init__(context)
        self._init_time = time.time()
        self._audio_timer = EventTimer()
        self._timeout_timer = EventTimer()

    def init_layout(self, canvas):
        self._title_label = canvas.set_widget(LabelWidget(_ALARM_LABEL * 3), 0)
        self._time_label = canvas.set_widget(LabelWidget(_time_text()), 1)
        self.poll_timer.timeout = 0.025

    def event_enter(self):
        self._audio_timer.reset_timeout(10)
        self._timeout_timer.reset_timeout(180)

    def event_exit(self):
        self.get_context().audio.stop()

    def event_button(self, stack, buttons):
        if buttons.only([Button.OK, Button.CANCEL]):
            stack.collapse()
        elif buttons.up(Button.CANCEL) and buttons.any():
            stack.push(AlarmSleepScreen(self.get_context()))

    def event_poll(self, stack, buttons):
        if self._audio_timer.expired():
            self.get_context().audio.start_alarm()
            self._audio_timer.disable()
        elif self._timeout_timer.expired():
            stack.collapse()
        else:
            offset = int((time.time() - self._init_time) * 20) % len(_ALARM_LABEL)
            self._title_label.text = _ALARM_LABEL[offset:] + (_ALARM_LABEL * 2)
            self._time_label.text = _time_text()
            self.repaint()

class AlarmSleepScreen(BasicScreen):
    def __init__(self, context):
        super(AlarmSleepScreen, self).__init__(context)

    def init_layout(self, canvas):
        base_sleep_time = self.settings["sleep_time"]

        self._sleep_time = time.time() + base_sleep_time
        self._time_label = canvas.set_widget(LabelWidget(_time_text()), 0)
        self._sleep_label = canvas.set_widget(LabelWidget(self.sleep_text()), 1)
        self.poll_timer.timeout = 1
                
    def event_button(self, stack, buttons):
        remaining = self._sleep_time - time.time()
        if buttons.only([Button.OK, Button.CANCEL]):
            stack.collapse()
        elif buttons.down(Button.LEFT) and remaining > 60:
            self._sleep_time -= 60
            self.update()
        elif buttons.down(Button.RIGHT):
            self._sleep_time += 60
            self.update()

    def event_poll(self, stack, buttons):
        remaining = self._sleep_time - time.time()
        if remaining <= 0:
            stack.pop()
        else:
            self.update()

    def sleep_text(self):
        remaining = self._sleep_time - time.time()
        
        min_str = ("%d" % int(remaining / 60)) if remaining >= 60 else ""
        sec_str = ("%02d" % int(remaining % 60))

        return "Sleep " + min_str + ":" + sec_str

    def update(self):
        self._time_label.text = _time_text()
        self._sleep_label.text = self.sleep_text()
        self.repaint()









