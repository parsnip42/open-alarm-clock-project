from widget import Widget
from focus_list import FocusList

class WidgetContainer(Widget):
    def __init__(self):
        super(WidgetContainer, self).__init__(highlight_focus=False)
        self.container_set_widgets([])

    def container_set_widgets(self, widgets):
        self._widgets = widgets
        self._focus_list = FocusList(widgets)

    def container_get_widgets(self):
        return self._widgets

    def set_focus(self, focused):
        self._focus_list.set_focus(focused)

    def prev_widget(self):
        return self._focus_list.prev_widget()

    def next_widget(self):
        return self._focus_list.next_widget()

    def current_widget(self):
        return self._focus_list.current_widget()
