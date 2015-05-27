from json import JSONDecoder
from datetime import date
from alarm import Alarm

class CommonJSONDecoder(JSONDecoder):
    def __init__(self, encoding):
        super(CommonJSONDecoder, self).__init__(encoding,
                                                object_hook=self.object_hook)

    def object_hook(self, obj):
        if obj.keys() == ["alarm"]:
            return self.decode_alarm_obj(obj["alarm"])
        else:
            return obj

    def decode_alarm_obj(self, obj):
        try:
            alarm = Alarm(str(obj["id"]),
                          int(obj["hour"]),
                          int(obj["minute"]),
                          tag=str(obj["tag"]),
                          editable=bool(obj["editable"]))
            
            if "days" in obj:
                alarm.days = Alarm.from_day_str(str(obj["days"]))
                
            if ("day" in obj) and \
               ("month" in obj) and \
               ("year" in obj):

                alarm.date = date(int(obj["year"]),
                                  int(obj["month"]),
                                  int(obj["day"]))

            return alarm

        except KeyError:
            raise ValueError
