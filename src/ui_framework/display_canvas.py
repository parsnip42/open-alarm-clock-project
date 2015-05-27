class DisplayCanvas:
    def __init__(self, display):
        self._display = display
        self._widgets = [None, None]

    def set_widget(self, widget, line):
        self._widgets[line] = widget
        return widget

    def get_root_widgets(self):
        return self._widgets

    def repaint(self):
        display = self._display

        for i in range(0, len(self._widgets)):
            if self._widgets[i] != None:
                self._display.text(self._widgets[i].widget_get_paint_str(display.width(i)), i)
            else:
                self._display.text("", i)

    def clear(self):
        self._widgets = [None, None]








