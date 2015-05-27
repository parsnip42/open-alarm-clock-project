from widget import Widget

class ToggleWidget(Widget):
    def __init__(self, selected_text, unselected_text, selected = False, update_func = None):
        super(ToggleWidget, self).__init__()
        self.selected_text = selected_text
        self.unselected_text = unselected_text
        self.selected = selected
        self._update_func = update_func

    def next(self):
        self._toggle()
        return True

    def prev(self):
        self._toggle()
        return True

    def get_paint_str(self, max_width):
        return self.selected_text if self.selected else self.unselected_text

    def _toggle(self):
        self.selected = not self.selected
        if self._update_func:
            self._update_func()











