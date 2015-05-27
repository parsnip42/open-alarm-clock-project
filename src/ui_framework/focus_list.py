class FocusList(object):
    def __init__(self, widgets = [], initial = 0):
        self.widgets = [w for w in widgets if w.widget_can_focus()]
        self.focus_index = initial

    def prev_widget(self):
        if self._current().prev_widget():
            return True               

        if self.at_first():
            return False

        self._move(-1)
        return True

    def next_widget(self):
        if self._current().next_widget():
            return True

        if self.at_last():
            return False
        
        self._move(1)
        return True

    def at_first(self):
        return self.focus_index == 0
    
    def at_last(self):
        return self.focus_index == (len(self.widgets) - 1)

    def current_widget(self):
        widget = self.widgets[self.focus_index]
        return widget.current_widget() or widget

    def _move(self, amount):
        self.set_focus(False)
        self.focus_index = (self.focus_index + amount) % len(self.widgets)
        self.set_focus(True)

    def _current(self):
        return self.widgets[self.focus_index]

    def set_focus(self, focus):
        if self.focus_index >= 0 and self.focus_index < len(self.widgets):
            widget = self.widgets[self.focus_index]
            widget.widget_set_focus(focus)












