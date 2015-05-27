from common import Alarm
from alarm_widgets import TimeEntry24Widget
from alarm_widgets import DaySelectWidget
from alarm_widgets import DateSelectWidget
from entry_screen import EntryScreen
from dialog_screen import OKCancelDialogScreen

class EditAlarmScreen(EntryScreen):
    def __init__(self, context, alarm, alarm_created_func):
        self._alarm_id = alarm.alarm_id
        self._time_widget = TimeEntry24Widget(alarm)

        if alarm.repeating:
            self._day_widget = DaySelectWidget(alarm)
        else:
            self._day_widget = DateSelectWidget(alarm)

        self._alarm_created_func = alarm_created_func

        super(EditAlarmScreen, self).__init__(context)

    def init_layout(self, canvas):
        canvas.set_widget(self._time_widget, 0)
        canvas.set_widget(self._day_widget, 1)

    def apply_changes(self, stack):
        alarm = Alarm(self._alarm_id,
                      self._time_widget.hour,
                      self._time_widget.minute)

        self._day_widget.get_contents(alarm)

        stack.push(OKCancelDialogScreen(self._context,
                                        alarm.description(),
                                        lambda: self._alarm_created_func(alarm)))

