import calendar
import datetime


class UserBirthday:
    def __init__(self, user_id, birthday_date, server_id):
        self.user_id = user_id
        self.birthday_date = birthday_date  # mm-dd
        self.server_id = server_id

    def __eq__(self, other):
        return self.user_id == other.user_id and other.server_id == self.server_id

    def get_datetime_date(self):
        if datetime.date(datetime.datetime.now().year, self.get_month_number(),
                         self.get_day_number()) < datetime.date.today():
            return datetime.date(datetime.datetime.now().year + 1, self.get_month_number(), self.get_day_number())
        else:
            return datetime.date(datetime.datetime.now().year, self.get_month_number(), self.get_day_number())

    def get_month_number(self):
        return int(self.birthday_date[0:2])

    def get_readable_month(self):
        return calendar.month_name[self.get_month_number()]

    def get_day_number(self):
        return int(self.birthday_date[3:5])

    def get_readable_day(self):
        day = str(self.get_day_number())
        if day == 1 or day == 31:
            day = day + "st"
        elif day == 2 or day == 22:
            day = day + "nd"
        elif day == 3 or day == 23:
            day = day + "rd"
        else:
            day = day + "th"

        return day
