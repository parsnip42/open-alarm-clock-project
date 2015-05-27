from common import Focus

class Widget(object):
    # Be sure to call this first in your subclassed widget.
    def __init__(self, can_focus = True, highlight_focus = True):
        self._can_focus = can_focus
        self._highlight_focus = can_focus and highlight_focus
        self._focused = False

    # Override any of these below to recieve an event.
    # Return True to consume the event.
    def prev(self):
        return False

    def next(self):
        return False

    # The two _repeat functions are entered only if prev/next
    # are not consumed. These are for autorepeat.
    def prev_repeat(self):
        return False

    def next_repeat(self):
        return False

    # Used by container widgets containing other widgets.
    def prev_widget(self):
        return False

    def next_widget(self):
        return False

    # The widget currently selected in this container, or
    # None if not applicable.
    def current_widget(self):
        return None

    # Called after changing focus.
    # Most of the time, you won't need to change this.
    def set_focus(self, focused):
        pass

    # When a widget has focus, it can poll for animation.
    # Return True to call poll() repeatedly on the widget.
    def polling(self):
        return False

    def poll(self, poll_time):
        pass

    # Override this to set the displayed text for your widget.
    def get_paint_str(self, max_width):
        return ""

    # Don't override any of the functions below prefixed
    # with "widget_"!
    def widget_can_focus(self):
        return self._can_focus

    def widget_set_focus(self, focused):
        self._focused = focused
        self.set_focus(focused)

    def widget_get_paint_str(self, max_width):
        value_str = self.get_paint_str(max_width)

        if self._highlight_focus and self._focused:
            if len(value_str) > max_width - 2:
                value_str = value_str[0:(max_width - 2)]
            value_str = Focus.LEFT + value_str + Focus.RIGHT

        return value_str[0:max_width]

















