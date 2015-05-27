import time

class EventTimer(object):
    NO_TIMEOUT = -1

    def __init__(self, timeout = NO_TIMEOUT):
        self._time = time.time()
        self.timeout = timeout

    def loop(self):
        self.timeout = 0

    def disable(self):
        self.timeout = EventTimer.NO_TIMEOUT

    def reset(self):
        self._time = time.time()

    def reset_timeout(self, timeout):
        self._time = time.time()
        self.timeout = timeout

    def remaining(self):
        if self.timeout == EventTimer.NO_TIMEOUT:
            return 10000
        else:
            return max(self.timeout - (time.time() - self._time), 0)

    def expired(self):
        return (self.timeout != -1) and ((time.time() - self._time) > self.timeout)














