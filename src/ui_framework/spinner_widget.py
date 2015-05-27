from widget import Widget

class SpinnerWidget(Widget):
    def __init__(self, value = 0, min_value = 0, max_value = 100, numformat = "%d", update_func = None):
        super(SpinnerWidget, self).__init__()

        self.value = value
        self.min_value = min_value
        self.max_value = max_value
        self._numformat = numformat
        self._update_func = update_func

    @property
    def min_value(self):
        return self._min_value

    @min_value.setter
    def min_value(self, value):
        self._min_value = value
        self.value = max(self.value, self.min_value)

    @property
    def max_value(self):
        return self._max_value

    @max_value.setter
    def max_value(self, value):
        self._max_value = value
        self.value = min(self.value, self.max_value)

    def next_repeat(self):
        self._spin(1)
        return True

    def prev_repeat(self):
        self._spin(-1)
        return True

    def get_paint_str(self, max_width):
        return self._numformat % self.value

    def _spin(self, increment):
        self.value += increment
        self.value = ((self.value - self.min_value) % ((self.max_value + 1) - self.min_value)) + self.min_value
        if self._update_func:
            self._update_func()









