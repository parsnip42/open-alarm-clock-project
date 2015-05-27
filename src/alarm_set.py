from datetime import datetime
from datetime import timedelta

class AlarmSet:
    class Entry:
        def __init__(self, alarm):
            self.alarm = alarm
            self.last = datetime.now()
            
        def next_fire(self):
            return self.alarm.next(self.last)

        def upcoming(self, now):
            next_fire = self.next_fire()
            return (next_fire != None) and (next_fire - now) < timedelta(hours=12)

    def __init__(self, settings):
        self._settings = settings
        self.load()

    def next_alarm(self):
        now = datetime.now()
        
        next_alarm = None
        next_fire = 10000000

        for entry in self._alarms.values():
            alarm = entry.alarm
            alarm_next = entry.next_fire()
            if alarm_next != None:
                fire_time = (alarm_next - now).total_seconds()
                if fire_time < next_fire:
                    next_alarm = alarm
                    next_fire = fire_time
        
        return (next_alarm, next_fire)
            
    def add_alarm(self, alarm):
        self._alarms[alarm.alarm_id] = self.Entry(alarm)
        self.save()

    def update_alarm(self, alarm):
        self._alarms[alarm.alarm_id] = self.Entry(alarm)
        self.save()

    def delete_alarm(self, alarm):
        del self._alarms[alarm.alarm_id]
        self.save()

    def clear_alarm(self, alarm):
        self._alarms[alarm.alarm_id].last = datetime.now()
        self.save()
    
    def defer_alarm(self, alarm):
        entry = self._alarms[alarm.alarm_id]
        entry.last = entry.next_fire()

    def renew_all(self):
        for entry in self._alarms.values():
            alarm = entry.alarm
            self.clear_alarm(alarm)

    def alarm_list(self):
        return sorted([item[1].alarm for item in self._alarms.items()],
                      key=lambda alarm: alarm.time)

    def upcoming_alarm_list(self):
        now = datetime.now()

        upcoming = [item[1] for item in self._alarms.items() if item[1].upcoming(now)]
        return [entry.alarm for entry in
                sorted(upcoming, key=lambda entry: entry.next_fire())]

    def count(self):
        return len(self._alarms)

    def count_upcoming(self):
        now = datetime.now()

        count = 0
        for entry in self._alarms.values():
            if entry.upcoming(now):
                count += 1

        return count

    def load(self):
        self._alarms = {}

        for alarm in self._settings['alarms']:
            self.add_alarm(alarm)

    def save(self):
        self._settings['alarms'] = self.alarm_list()
