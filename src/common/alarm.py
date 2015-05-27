from datetime import datetime
from datetime import timedelta
from datetime import time
import uuid

class Alarm:
    MONDAY    = 1
    TUESDAY   = 1 << 1
    WEDNESDAY = 1 << 2
    THURSDAY  = 1 << 3
    FRIDAY    = 1 << 4
    SATURDAY  = 1 << 5
    SUNDAY    = 1 << 6

    WEEKDAYS = MONDAY | TUESDAY | WEDNESDAY | THURSDAY | FRIDAY
    WEEKENDS = SATURDAY | SUNDAY
    ALL_DAYS = WEEKDAYS | WEEKENDS

    DAYS = [ "M", "T", "W", "T", "F", "S", "S" ]

    @staticmethod
    def new_id():
        return str(uuid.uuid1())

    @staticmethod
    def to_day_str(days):
        return "".join([day if (days & (1 << index)) else "-"
                        for index, day in enumerate(Alarm.DAYS)])

    @staticmethod
    def from_day_str(day_str):
        days = 0
        for index, day in enumerate(day_str):
            if day == Alarm.DAYS[index]:
                days |= (1 << index)

        return days

    def __init__(self, alarm_id, hour, minute, days = 0, date = None, tag = "", editable = True):
        self.alarm_id = alarm_id
        self.time = time(hour, minute, 0)
        self.days = days
        self.date = date
        self.tag = tag
        self.editable = editable
        
    @property
    def repeating(self):
        return self.date == None

    def on_day(self, day):
        return bool(self.days & (1 << day))

    def next_date(self, last):
        if self.days != 0:
            day_mask = (self.days | (self.days << 7)) >> last.weekday()
            next_date = last.date()
            while not(day_mask & 1):
                day_mask >>= 1
                next_date += timedelta(days=1)
            
            return next_date
        
        elif self.date != None and self.date >= last.date():
            return self.date

        else:
            return None

    def next(self, last):
        if self.time > last.time():
            next_date = self.next_date(last)
        else:
            next_date = self.next_date(last + timedelta(days=1))

        if next_date != None:
            return datetime.combine(next_date, self.time)
        else:
            return None

    def date_description(self):
        if self.date == None:
            return Alarm.to_day_str(self.days)
        else:
            now = datetime.now()
            return datetime.strftime(datetime.combine(self.date, now.time()), "%d %b")

    def description(self):
        return (("%02d" % self.time.hour) +
                ":" +
                ("%02d" % self.time.minute) +
                " " +
                self.date_description())
                
                

