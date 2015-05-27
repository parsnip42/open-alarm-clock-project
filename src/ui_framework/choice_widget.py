from widget import Widget

class ChoiceWidget(Widget):
    def __init__(self, items, selected_index = 0, update_func = None):
        super(ChoiceWidget, self).__init__()

        if len(items) == 0:
            self.items = [ ("", None) ]
        else:
            self.items = items

        self.selected_index = selected_index
        self._update_func = update_func 

    def prev_repeat(self):
        self._spin(-1)
        return True

    def next_repeat(self):
        self._spin(1)
        return True

    @property
    def selected_item(self):
        return self.items[self.selected_index][1]

    @selected_item.setter
    def selected_item(self, value):
        for (index, item) in enumerate(self.items):
            if item[1] == value:
                self.selected_index = index
                break

    def get_paint_str(self, max_width):
        return self.items[self.selected_index][0]

    def _spin(self, increment):
        self.selected_index = ((self.selected_index + increment) % len(self.items))
        if self._update_func:
            self._update_func()










