import os
import json


# noinspection PyArgumentList
class Settings(object):
    default_bot_settings_file = "data/settings.json"
    default_bot_notification_time = 11  # hour of the day i.e 11am
    default_bot_volume = 0.25

    json_notification_time = "default_notification_time"
    json_volume = "default_volume"
    json_command_states = "command_states"

    def __init__(self):
        self.default_user_notification_time = None
        self.default_user_volume = None
        self.user_command_states = None

        self.json_settings_defaults = None

        self.get_user_defaults()

    @staticmethod
    def get_default_option(user_option, app_option):
        if user_option is None:
            return app_option
        else:
            return user_option

    def get_default_notification_time(self):
        return self.get_default_option(self.default_user_notification_time, self.default_bot_notification_time)

    def get_default_volume(self):
        return self.get_default_option(self.default_user_volume, self.default_bot_volume)

    def get_user_defaults(self):
        if not os.path.exists(self.default_bot_settings_file):
            return

        with open(self.default_bot_settings_file, 'r') as file:
            if os.stat(self.default_bot_settings_file).st_size == 0:  # If the file is empty
                return

            self.json_settings_defaults = json.load(file)

            self.default_user_notification_time = self.set_user_default(self.json_notification_time)
            self.default_user_volume = self.set_user_default(self.json_volume)
            self.user_command_states = self.set_user_default(self.json_command_states)

    def save_user_defaults(self, notification_time=None, volume=None, command_state=None):
        if notification_time is None:
            notification_time = self.get_default_notification_time()
        else:
            self.default_user_notification_time = notification_time

        if volume is None:
            volume = self.get_default_volume()
        else:
            self.default_user_volume = volume

        # format: {'cmd_name':name, 'enabled':'False'}
        # Should never be True
        if command_state is not None:
            if self.user_command_states is None:
                self.user_command_states = [command_state]
            else:
                self.user_command_states.append(command_state)

        info_dicts = {self.json_notification_time: notification_time,
                      self.json_volume: volume,
                      self.json_command_states: self.user_command_states}
        json_string = json.dumps(info_dicts, indent=4, separators=(',', ' : '))

        with open(self.default_bot_settings_file, 'w') as file:
            file.write(json_string)

    def delete_command_state(self, cmd_state):
        try:
            self.user_command_states.remove(cmd_state)
        except ValueError:
            return
        info_dicts = {self.json_notification_time: self.default_user_notification_time,
                      self.json_volume: self.default_user_volume,
                      self.json_command_states: self.user_command_states}
        json_string = json.dumps(info_dicts, indent=4, separators=(',', ' : '))

        with open(self.default_bot_settings_file, 'w') as file:
            file.write(json_string)

    def set_user_default(self, option_name):
        try:
            return self.json_settings_defaults[option_name]
        except KeyError:
            return None
