from common import Alarm
from ui_framework import WidgetSet
from ui_framework import ToggleWidget

class DaySelectWidget(WidgetSet):
    def __init__(self, alarm):
        super(DaySelectWidget, self).__init__()
        self._buttons = [ToggleWidget(day, "-", True) for day in Alarm.DAYS]
        self.container_set_widgets(self._buttons)
        self.set_contents(alarm)

    def get_contents(self, alarm):
        alarm.days = self.days

    def set_contents(self, alarm):
        self.days = alarm.days

    @property
    def days(self):
        return sum([2**index
                    for index, button in enumerate(self._buttons)
                    if button.selected])

    @days.setter
    def days(self, value):
        for index, button in enumerate(self._buttons):
            button.selected = bool(value & (1 << index))


