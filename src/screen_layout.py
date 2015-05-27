from datetime import datetime
from os_utils import OSUtils
from common import Alarm
from home_screen import HomeScreen
from menu_screen import MenuScreen
from setting_selection_screen import SettingSelectionScreen
from edit_alarm_screen import EditAlarmScreen
from dialog_screen import OKCancelDialogScreen
from dialog_screen import OKDialogScreen
from dialog_screen import FixedDialogScreen

def get_base(context):
    def push_screen(screen):
        context.stack.push(screen)

    def pop_after(func):
        return lambda: (func(), context.stack.pop())

    def collapse_after(func):
        return lambda: (func(), context.stack.collapse())

    def alarm_sound_handler():
        items = context.audio.get_audio_files()
        
        if items:
            push_screen(SettingSelectionScreen(context,
                                               context.settings,
                                               'Alarm Sound',
                                               'alarm_sound',
                                               items))
        else:
            push_screen(OKDialogScreen(context, 'No Sounds')),

    def audio_test_handler():
        context.audio.audio_test()
        push_screen(OKDialogScreen(context, 'Audio Test',
                                   pop_after(context.audio.stop)))

    def display_type_handler():
        items = [ ('Date/Time', 'date_time'),
                  ('Time Only', 'time'),
                  ('Blank', 'blank') ]

        push_screen(SettingSelectionScreen(context,
                                           context.settings,
                                           'Display Type',
                                           'display_type',
                                           items))

    def settings_handler():
        push_screen(MenuScreen(context, 'Settings', [
                    ('Alarm Sound', alarm_sound_handler),
                    ('Audio Test', audio_test_handler),
                    ('Display Type', display_type_handler),
                    ('System', system_handler)
                    ]))

    def system_handler():
        def confirm_cmd(title, message, action):
            return lambda: push_screen(OKCancelDialogScreen(context, title,
                           lambda: (push_screen(FixedDialogScreen(context, message)), action())))
            
        push_screen(MenuScreen(context, 'System', [
                    ('Reboot', confirm_cmd('Reboot?', 'Reboot', OSUtils.reboot)),
                    ('Shutdown', confirm_cmd('Shutdown?', 'Shutdown', OSUtils.shutdown))
                    ]))

    def alarm_updated_handler(alarm):
        context.alarms.update_alarm(alarm)
        context.alarms.save()
        context.stack.collapse()

    def edit_alarm_handler(alarm):
        if alarm.editable:
            push_screen(EditAlarmScreen(context, alarm, alarm_updated_handler))

    def delete_alarm_handler(alarm):
        def do_delete():
            context.alarms.delete_alarm(alarm)
            context.alarms.save()
            context.stack.collapse()

        push_screen(OKCancelDialogScreen(context,
                                         'Delete Alarm?',
                                         do_delete))

    def alarm_selected_handler(alarm):
        push_screen(MenuScreen(context, alarm.description(), [
                    ('Renew Alarm', pop_after(lambda: context.alarms.clear_alarm(alarm))),
                    ('Edit Alarm', lambda: edit_alarm_handler(alarm) ),
                    ('Delete Alarm', lambda: delete_alarm_handler(alarm))
                    ]))

    def alarm_created_handler(alarm):
        context.alarms.add_alarm(alarm)
        context.alarms.save()
        context.stack.collapse()

    def new_single_handler():
        now = datetime.now()
        alarm = Alarm(Alarm.new_id(), now.hour, now.minute, date=now.date())
        push_screen(EditAlarmScreen(context, alarm, alarm_created_handler))

    def new_weekly_handler():
        alarm = Alarm(Alarm.new_id(), 12, 0, days=Alarm.WEEKDAYS)
        push_screen(EditAlarmScreen(context, alarm, alarm_created_handler))

    def alarm_setup_handler():
        alarm_list = context.alarms.alarm_list()
        
        def create_selected_handler(alarm):
            return lambda: alarm_selected_handler(alarm)

        alarm_menu_items = [ (alarm.description(), create_selected_handler(alarm))
                              for alarm in alarm_list ]

        push_screen(MenuScreen(context,
                               'Alarms',
                               [ ('New Single', new_single_handler),
                                 ('New Weekly', new_weekly_handler) ] +
                               alarm_menu_items ))

    def pending_alarm_selected_handler(alarm):
        push_screen(MenuScreen(context, alarm.description(), [
                    ('Defer Alarm', collapse_after(lambda: context.alarms.defer_alarm(alarm))),
                    ('Edit Alarm', lambda: edit_alarm_handler(alarm)),
                    ('Delete Alarm', lambda: delete_alarm_handler(alarm))]))

    def pending_alarms_handler():
        def create_selected_handler(alarm):
            return lambda: pending_alarm_selected_handler(alarm)

        alarm_menu_items = [ (alarm.description(), create_selected_handler(alarm))
                              for alarm in context.alarms.upcoming_alarm_list() ]

        push_screen(MenuScreen(context,
                               'Pending Alarms',
                               [ ('Renew All', collapse_after(context.alarms.renew_all)) ] +
                               alarm_menu_items))

    def menu_handler():
        push_screen(MenuScreen(context, 'Main Menu', [
                    ('Pending Alarms', pending_alarms_handler),
                    ('Alarm Setup', alarm_setup_handler),
                    ('Settings', settings_handler),
                    ]))

        
    return HomeScreen(context, menu_handler)
