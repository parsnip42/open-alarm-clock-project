from json import JSONEncoder
from alarm import Alarm

class CommonJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Alarm):
            out = {"id": obj.alarm_id,
                   "hour": obj.time.hour,
                   "minute": obj.time.minute,
                   "tag": obj.tag,
                   "editable": obj.editable}

            if obj.days != 0:
                out["days"] = Alarm.to_day_str(obj.days)

            if obj.date:
                out["day"] = obj.date.day
                out["month"] = obj.date.month
                out["year"] = obj.date.year

            return {"alarm": out}
        else:
            return super(CommonJSONEncoder, self).default(self, obj)
