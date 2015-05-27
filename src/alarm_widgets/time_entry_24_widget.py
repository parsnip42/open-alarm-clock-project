from ui_framework import WidgetSet
from ui_framework import LabelWidget
from ui_framework import SpinnerWidget

class TimeEntry24Widget(WidgetSet):
    def __init__(self, alarm):
        super(TimeEntry24Widget, self).__init__()
        self._hour_widget = SpinnerWidget(0, 0, 23, "%02d")
        self._minute_widget = SpinnerWidget(0, 0, 59, "%02d")
        self.container_set_widgets([self._hour_widget,
                                    LabelWidget(":"),
                                    self._minute_widget])

        self.hour = alarm.time.hour
        self.minute = alarm.time.minute

    @property
    def hour(self):
        return self._hour_widget.value

    @hour.setter
    def hour(self, value):
        self._hour_widget.value = value
    
    @property
    def minute(self):
        return self._minute_widget.value

    @minute.setter
    def minute(self, value):
        self._minute_widget.value = value

