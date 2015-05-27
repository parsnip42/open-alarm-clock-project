from ui_common import Event

class ScreenStack:
    def __init__(self):
        self.base = None;
        self.stack = []
        
    def push(self, screen):
        self.current().event(Event.EXIT, None)
        self.stack.append(screen)
        screen.event(Event.ENTER, None)

    def pop(self):
        if len(self.stack) > 0:
            self.stack.pop().event(Event.EXIT, None)
            self.current().event(Event.ENTER, None)
    
    def collapse(self):
        if len(self.stack) > 0:
            self.stack.pop().event(Event.EXIT, None)
            self.stack = []
            self.current().event(Event.ENTER, None)

    def current(self):
        stack_len = len(self.stack)
        return self.stack[stack_len - 1] if stack_len > 0 else self.base

    def empty(self):
        return len(self.stack) == 0









