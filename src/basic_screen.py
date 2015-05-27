from ui_common import Event
from event_timer import EventTimer
from ui_framework import DisplayCanvas

class ButtonState(object):
    def __init__(self):
        self.reset()
    
    def event(self, event, event_args):
        if event == Event.BUTTON_DOWN:
            self._button_mask |= (1 << event_args)
        elif event == Event.BUTTON_UP:
            self._button_mask &= ~(1 << event_args)

    def reset(self):
        self._button_mask = 0

    def any(self):
        return self._button_mask != 0

    def only(self, buttons):
        return (self._button_mask == reduce(lambda x, y: x | y,
                                            [(1 << button) for button in buttons]))

    def down(self, button):
        return (self._button_mask & (1 << button)) != 0

    def single_down(self, button):
        down = (self._button_mask & (1 << button)) != 0
        self._button_mask &= ~(1 << button)

        return down

    def up(self, button):
        return not self.down(button)

class BasicScreen(object):
    def __init__(self, context):
        self._context = context
        self._buttons = ButtonState()
        self._canvas = DisplayCanvas(context.display)
        self.poll_timer = EventTimer()
        self.init_layout(self._canvas)

    def event(self, event, event_args):
        self._buttons.event(event, event_args)

        { Event.ENTER:
              lambda: (self._buttons.reset(),
                       self.event_enter(),
                       self.repaint()),
          Event.EXIT:
              lambda: self.event_exit(),
          Event.BUTTON_UP:
              lambda: self.event_button(self._context.stack,
                                        self._buttons),
          Event.BUTTON_DOWN:
              lambda: self.event_button(self._context.stack,
                                        self._buttons),
          Event.POLL: lambda:
              self.event_poll(self._context.stack,
                              self._buttons)
          }.get(event, lambda: None)()

    def repaint(self):
        self._canvas.repaint()

    def get_root_widgets(self):
        return [w for w in self._canvas.get_root_widgets() if w != None]

    def get_context(self):
        return self._context

    @property
    def settings(self):
        return self._context.settings

    def poll_timer(self):
        return self.poll_timer()

    def init_layout(self, canvas):
        pass

    def event_enter(self):
        pass

    def event_exit(self):
        pass

    def event_button(self, stack, buttons):
        pass

    def event_poll(self, stack, buttons):
        pass
    
