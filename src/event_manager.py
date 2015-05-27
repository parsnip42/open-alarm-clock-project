import Queue
from datetime import datetime
from event_timer import EventTimer
from screen_stack import ScreenStack
from screen_context import ScreenContext
from ui_common import Event
from alarm_screen import AlarmScreen
import screen_layout

class EventManager(object):
    def __init__(self, settings, device):
        self._device = device
        self._event_queue = Queue.Queue()
        self._stack = ScreenStack()
        self._active_alarm = False
        self._settings = settings

        context = ScreenContext(settings,
                                self._stack,
                                device.display)

        self._context = context
        self._stack.base = screen_layout.get_base(context)

    def post_event(self, event, event_args = None):
        self._event_queue.put((event, event_args))

    def start(self):
        self._stack.current().event(Event.ENTER, None)
        
        inactivity_timeout = self._settings["inactivity_timeout"]
        inact_timer = EventTimer(inactivity_timeout)
        alarm_timer = EventTimer(0)

        while True:
            if self._stack.empty():
                inact_timer.disable()
            else:
                inact_timer.timeout = inactivity_timeout

            try:
                current = self._stack.current()
                timers = [current.poll_timer, inact_timer, alarm_timer]
                queue_timeout = min([timer.remaining() for timer in timers])
                event_tuple = self._event_queue.get(True, queue_timeout)

                if event_tuple[0] == Event.SHUTDOWN:
                    return

                if Event.user_event(event_tuple[0]):
                    inact_timer.reset()

                current.event(event_tuple[0], event_tuple[1])

            except Queue.Empty:
                pass

            poll_timer = self._stack.current().poll_timer
            if poll_timer.expired():
                poll_timer.reset()
                current.event(Event.POLL, None)

            if inact_timer.expired():
                inact_timer.reset()
                if not self._active_alarm:
                    self._stack.collapse()

            if alarm_timer.expired():
                self._check_alarms()
                alarm_timer.timeout = (60 - datetime.now().second)
                alarm_timer.reset()

        self._stack.current().event(Event.EXIT, None)

    def stop(self):
        self._context.audio.stop()
        self.post_event(Event.SHUTDOWN)

    def _check_alarms(self):
        (alarm, fire_time) = self._context.alarms.next_alarm()

        if alarm != None and fire_time <= 0:
            self._active_alarm = True
            self._stack.push(AlarmScreen(self._context))

            if alarm.repeating or not self._settings["delete_expired_alarms"]:
                self._context.alarms.clear_alarm(alarm)
            else:
                self._context.alarms.delete_alarm(alarm)










