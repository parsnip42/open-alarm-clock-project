from settings import Settings
from common import Alarm

class DefaultSettings:
    @staticmethod
    def populate(settings):
        settings.define(Settings.Entry("display_type", str, ""))
        settings.define(Settings.Entry("inactivity_timeout", int, 15))
        settings.define(Settings.Entry("sleep_time", int, 60 * 9))
        settings.define(Settings.Entry("delete_expired_alarms", bool, True))
        settings.define(Settings.Entry("alarms", Alarm, [], True))
        settings.define(Settings.Entry("alarm_sound", str, ""))
