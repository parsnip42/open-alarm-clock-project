class MultiTimer(object):
    def __init__(self, timers):
        self._timers = timers

    def reset(self):
        pass

    def remaining(self):
        if self._timers == []:
            return 10000
        else:
            return min([timer.remaining() for timer in self._timers])
    
    def expired(self):
        if self._timers == []:
            return False
        else:
            return max([timer.timeout for timer in self._timers])
