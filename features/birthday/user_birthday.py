import calendar
import datetime
import pytz


class UserBirthday:
    def __init__(self, user_id, birthday_date, server_id):
        self.user_id = user_id
        self.birthday_date = birthday_date  # mm-dd
        self.server_id = server_id

    def __eq__(self, other):
        return self.user_id == other.user_id and other.server_id == self.server_id

    @property
    def current_year(self):
        return datetime.datetime.now(pytz.timezone('EST')).year

    def get_astrological_sign(self):
        # Requested by Waffle.
        if datetime.date(self.current_year, 3, 21) <= self.get_datetime_date_no_adjustment() <= datetime.date(
                self.current_year, 4, 19):
            return "Aries ♈"
        elif datetime.date(self.current_year, 4, 20) <= self.get_datetime_date_no_adjustment() <= datetime.date(
                self.current_year, 5, 20):
            return "Taurus ♉"
        elif datetime.date(self.current_year, 5, 21) <= self.get_datetime_date_no_adjustment() <= datetime.date(
                self.current_year, 6, 20):
            return "Gemini ♊"
        elif datetime.date(self.current_year, 6, 21) <= self.get_datetime_date_no_adjustment() <= datetime.date(
                self.current_year, 7, 22):
            return "Cancer ♋"
        elif datetime.date(self.current_year, 7, 23) <= self.get_datetime_date_no_adjustment() <= datetime.date(
                self.current_year, 8, 22):
            return "Leo ♌"
        elif datetime.date(self.current_year, 8, 23) <= self.get_datetime_date_no_adjustment() <= datetime.date(
                self.current_year, 9, 22):
            return "Virgo ♍"
        elif datetime.date(self.current_year, 9, 23) <= self.get_datetime_date_no_adjustment() <= datetime.date(
                self.current_year, 10, 22):
            return "Libra ♎"
        elif datetime.date(self.current_year, 10, 23) <= self.get_datetime_date_no_adjustment() <= datetime.date(
                self.current_year, 11, 21):
            return "Scorpio ♏"
        elif datetime.date(self.current_year, 11, 22) <= self.get_datetime_date_no_adjustment() <= datetime.date(
                self.current_year, 12, 21):
            return "Sagittarius ♐"
        elif datetime.date(self.current_year, 12, 22) <= self.get_datetime_date() <= datetime.date(
                self.current_year + 1, 1, 19):  # Needs to use next year or it will return False
            return "Capricorn ♑"
        elif datetime.date(self.current_year, 1, 20) <= self.get_datetime_date_no_adjustment() <= datetime.date(
                self.current_year, 2, 18):
            return "Aquarius ♒"
        elif datetime.date(self.current_year, 2, 19) <= self.get_datetime_date_no_adjustment() <= datetime.date(
                self.current_year, 3, 20):
            return "Pisces ♓"
        else:
            return "Astrological sign broken?"

    def get_datetime_date(self):
        if datetime.datetime(self.current_year, self.get_month_number(),
                             self.get_day_number()) < datetime.datetime.today():
            return datetime.date(self.current_year + 1, self.get_month_number(), self.get_day_number())
        else:
            return datetime.date(self.current_year, self.get_month_number(), self.get_day_number())

    def get_datetime_date_no_adjustment(self):
        return datetime.date(datetime.datetime.now(pytz.timezone('EST')).year,
                             self.get_month_number(), self.get_day_number())

    def get_month_number(self):
        return int(self.birthday_date[0:2])

    def get_readable_month(self):
        return calendar.month_name[self.get_month_number()]

    def get_day_number(self):
        return int(self.birthday_date[3:5])

    def get_readable_day(self):
        day = int(self.get_day_number())
        if day == 1 or day == 21 or day == 31:
            day = str(day) + "st"
        elif day == 2 or day == 22:
            day = str(day) + "nd"
        elif day == 3 or day == 23:
            day = str(day) + "rd"
        else:
            day = str(day) + "th"

        return day

    def get_readable_date(self):
        return "{} {}, {}".format(self.get_readable_month(), self.get_readable_day(), self.current_year)
