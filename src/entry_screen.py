import time
from ui_common import Button
from ui_framework import FocusList
from basic_screen import BasicScreen

class RepeatTimer(object):
    def __init__(self):
        self._time = time.time()
        self.timeout = -1

    def start(self):
        self._time = time.time()
        self.timeout = 0.4

    def stop(self):
        self.timeout = -1

    def active(self):
        return self.timeout != -1

    def reset(self):
        self.timeout = max(self.timeout * 0.7, 0.05)
        self._time = time.time()

    def expired(self):
        return (self.timeout != -1) and ((time.time() - self._time) > self.timeout)

class EntryScreen(BasicScreen):
    def __init__(self, context):
        super(EntryScreen, self).__init__(context)
        self._repeat_timer = RepeatTimer()
        self._focus_list = FocusList(self.get_root_widgets())
        self._focus_list.set_focus(True)

    def event_button(self, stack, buttons):
        widget = self._focus_list.current_widget()

        if buttons.single_down(Button.OK):
            if self._focus_list.next_widget():
                self.repaint()
            else:
                self.apply_changes(self.get_context().stack)

        elif buttons.single_down(Button.CANCEL):
            if self._focus_list.prev_widget():
                self.repaint()
            else:
                stack.pop()

        if buttons.down(Button.LEFT) and widget.prev():
            self.repaint()
            buttons.reset()
        
        if buttons.down(Button.RIGHT) and widget.next():
            self.repaint()
            buttons.reset()
            
        if (buttons.down(Button.LEFT) and widget.prev_repeat()) or \
                (buttons.down(Button.RIGHT) and widget.next_repeat()):
            self._repeat_timer.start()
            self.repaint()
        else:
            self._repeat_timer.stop()

        if self._repeat_timer.active() or widget.polling():
            self.poll_timer.timeout = 0.01
        else:
            self.poll_timer.disable()

    def event_poll(self, stack, buttons):
        widget = self._focus_list.current_widget()

        if self._repeat_timer.expired():
            if (buttons.down(Button.RIGHT) and widget.next_repeat()) or \
                    (buttons.down(Button.LEFT) and widget.prev_repeat()):
                self.repaint()
                self._repeat_timer.reset()

        if widget.polling():
            widget.poll()
            self.repaint()
        elif not self._repeat_timer.active():
            self.poll_timer.disable()

    def apply_changes(self, stack):
        pass
