import calendar
import datetime
from ui_framework import WidgetSet
from ui_framework import LabelWidget
from ui_framework import ChoiceWidget
from ui_framework import SpinnerWidget

class DateSelectWidget(WidgetSet):
    def __init__(self, alarm):
        super(DateSelectWidget, self).__init__()
        self._day_widget = SpinnerWidget(1, 1, 31, "%02d")
        
        months = [(name[0:3], index)
                  for index, name in enumerate(calendar.month_name)][1:]
        self._month_widget = ChoiceWidget(months, update_func = self._month_changed)
        self.container_set_widgets([self._day_widget,
                                    LabelWidget(" "),
                                    self._month_widget])
        self.set_contents(alarm)

    def get_contents(self, alarm):
        try:
            alarm.date = datetime.date(self.year, self.month, self.day)
        except ValueError:
            pass

    def set_contents(self, alarm):
        date = alarm.date
        if date != None:
            self.day = date.day
            self.month = date.month

    @property
    def day(self):
        return self._day_widget.value

    @day.setter
    def day(self, value):
        self._day_widget.value = value

    @property
    def month(self):
        return self._month_widget.selected_index + 1

    @month.setter
    def month(self, value):
        self._month_widget.selected_index = value - 1

    @property
    def year(self):
        now = datetime.datetime.now()
        
        if self.month > now.month or \
                (self.month == now.month and self.day >= now.day):
            return now.year
        else:
            return now.year + 1

    def _month_changed(self):
        self._day_widget.max_value = calendar.monthrange(self.year, self.month)[1]
