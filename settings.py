import os
import json


# noinspection PyArgumentList
class Settings(object):
    default_bot_settings_file = "data/settings.json"
    default_bot_notification_time = 11  # hour of the day i.e 11am

    json_notification_time = "default_notification_time"

    def __init__(self):
        self.default_user_notification_time = None

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

    def get_user_defaults(self):
        if not os.path.exists(self.default_bot_settings_file):
            return

        with open(self.default_bot_settings_file, 'r') as file:
            if os.stat(self.default_bot_settings_file).st_size == 0:  # If the file is empty
                return

            self.json_settings_defaults = json.load(file)

            self.default_user_notification_time = self.set_user_default(self.json_notification_time)

    def save_user_defaults(self, notification_time=None):
        if notification_time is None:
            notification_time = self.get_default_notification_time()
        else:
            self.default_user_notification_time = notification_time

        info_dicts = {self.json_notification_time: notification_time}
        json_string = json.dumps(info_dicts, indent=4, separators=(',', ' : '))

        with open(self.default_bot_settings_file, 'w') as file:
            file.write(json_string)

    def set_user_default(self, option_name):
        try:
            return self.json_settings_defaults[option_name]
        except KeyError:
            return None
