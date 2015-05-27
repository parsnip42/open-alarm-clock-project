import time
from ui_framework import Widget
from ui_framework import LabelWidget
from ui_framework import ButtonWidget
from ui_framework import SpreadWidgetSet
from ui_framework import FocusList
from basic_screen import BasicScreen
from entry_screen import EntryScreen

class OptionSelectionWidget(Widget):
    def __init__(self, options):
        super(OptionSelectionWidget, self).__init__(highlight_focus=False)

        self._options = options
        widgets = [ButtonWidget(option[0]) for option in self._options]
        self._widget_set = SpreadWidgetSet(widgets)
        self._focus_list = FocusList(widgets)

    def prev(self):
        self._focus_list.prev_widget()
        return True

    def next(self):
        self._focus_list.next_widget()
        return True

    def set_focus(self, focused):
        self._focus_list.set_focus(focused)

    @property
    def selected_item(self):
        return self._options[self._focus_list.focus_index][1]

    def get_paint_str(self, max_width):
        return self._widget_set.get_paint_str(max_width)


class DialogScreen(EntryScreen):
    def __init__(self, context, message, options):
        self._message = message
        self._selection_widget = OptionSelectionWidget(options)
        super(DialogScreen, self).__init__(context)

    def init_layout(self, canvas):
        canvas.set_widget(LabelWidget(self._message), 0)
        canvas.set_widget(self._selection_widget, 1)

    def apply_changes(self, stack):
        (self._selection_widget.selected_item or stack.pop)()


class OKCancelDialogScreen(DialogScreen):
    def __init__(self, context, message, ok_func = None, cancel_func = None):
        options = [("OK", ok_func), ("Cancel", cancel_func)]
        super(OKCancelDialogScreen, self).__init__(context, message, options)


class OKDialogScreen(DialogScreen):
    def __init__(self, context, message, ok_func = None):
        options = [("OK", ok_func)]
        super(OKDialogScreen, self).__init__(context, message, options)


class FixedDialogScreen(BasicScreen):
    def __init__(self, context, message):
        self._message = message

        super(FixedDialogScreen, self).__init__(context)

    def init_layout(self, canvas):
        self._message_label = canvas.set_widget(LabelWidget(self._message), 0) 
        self.poll_timer.timeout = 0.25

    def event_poll(self, stack, buttons):
        self._message_label.text = self._message if (int(time.time() * 2) % 2) == 0 else ""
        self.repaint()




















