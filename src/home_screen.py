from datetime import datetime
from event_timer import EventTimer
from multi_timer import MultiTimer
from ui_common import Button
from ui_framework import Widget
from ui_framework import SingleWidgetContainer
from ui_framework import BorderedWidgetSet
from basic_screen import BasicScreen

class TimeoutFunc(object):
    @staticmethod
    def MINUTE(now):
        return 60 - now.second

    @staticmethod
    def SECOND(now):
        return 1
    
class DateTimeDisplay(Widget):
    def __init__(self, format_str, timeout_func):
        super(DateTimeDisplay, self).__init__(can_focus=False)
        self._format_str = format_str
        self._timeout_func = timeout_func
        self._paint_str = ""
        self.poll_timer = EventTimer(0)

    def update(self, now, context):
        self._paint_str = datetime.strftime(now, self._format_str)
        self.poll_timer.reset_timeout(self._timeout_func(now))

    def get_paint_str(self, max_width):
        return self._paint_str;

class UpcomingAlarmsDisplay(Widget):
    def __init__(self):
        super(UpcomingAlarmsDisplay, self).__init__(can_focus=False)
        self._paint_str = ""
        self.poll_timer = EventTimer(0)

    def update(self, now, context):
        alarm_count = context.alarms.count_upcoming()
        self._paint_str = "" if alarm_count <= 0 else chr(3) + str(alarm_count)
        self.poll_timer.reset_timeout(60 - now.second)

    def get_paint_str(self, max_width):
        return self._paint_str;

class HomeScreen(BasicScreen):
    def __init__(self, context, setup_func):
        super(HomeScreen, self).__init__(context)
        self._setup_func = setup_func
        self._disabled = False
        self._display_widgets = []

        self.poll_timer.reset_timeout(60 - datetime.now().second)

    def init_layout(self, canvas):
        self._date_line = canvas.set_widget(SingleWidgetContainer(), 0)
        self._time_line = canvas.set_widget(SingleWidgetContainer(), 1)

        self._date_label = DateTimeDisplay("%a %d %b %Y", TimeoutFunc.MINUTE)
        self._time_label = DateTimeDisplay("%H:%M", TimeoutFunc.MINUTE)
        self._status_label = UpcomingAlarmsDisplay()

    def event_enter(self):
        self._enable()

    def event_button(self, stack, buttons):
        if self._disabled and buttons.any():
            self._enable()
            buttons.reset()
        elif buttons.up(Button.CANCEL) and buttons.any():
            self._setup_func()
        elif buttons.only([Button.LEFT, Button.CANCEL]) or \
                buttons.only([Button.RIGHT, Button.CANCEL]):
            self._disable()
            buttons.reset()

    def event_poll(self, stack, buttons):
        now = datetime.now()
        context = self.get_context()
        for display in self._display_widgets:
            if display.poll_timer.expired():
                display.update(now, context)

        self.repaint()

    def _update_display_type(self):
        display_type = self.settings["display_type"]
        
        if display_type == "blank":
            self._date_line.clear()
            self._time_line.clear()
            self._display_widgets = []
        elif display_type == "time":
            self._date_line.clear()
            self._time_line.set_widget(BorderedWidgetSet(None, self._time_label, self._status_label))
            self._display_widgets = [self._time_label, self._status_label]
        else:
            self._date_line.set_widget(self._date_label)
            self._time_line.set_widget(BorderedWidgetSet(None, self._time_label, self._status_label))
            self._display_widgets = [self._date_label, self._time_label, self._status_label]

        now = datetime.now()
        context = self.get_context()
        for display in self._display_widgets:
            display.update(now, context)

        self.repaint()

    def _enable(self):
        self._update_display_type()

        self.poll_timer = MultiTimer([widget.poll_timer for widget in self._display_widgets])
        self._disabled = False

    def _disable(self):
        self._date_line.clear()
        self._time_line.clear()
        self.repaint()

        self.poll_timer = EventTimer()
        self._disabled = True






