import discord
import datetime
import os

import hidden


def code_format(code_header, content):
    return "```{}\n{}```".format(code_header, content)


def user_format(user_id):
    return "<@!{}>".format(user_id)


def channel_format(channel_id):
    return "<#{}>".format(channel_id)


def get_custom_emoji(client: discord.Client, name: str):
    for emoji in client.get_all_emojis():
        if emoji.name.lower() == name.lower():
            return emoji
    return None


def get_next_day_delta(hour: int):
    today_n = datetime.datetime.today()
    try:
        today_t = today_n.replace(day=today_n.day + 1, hour=hour, minute=0, second=0, microsecond=0)
    except ValueError:
        try:
            # Only time it will go there is at the end of the month, except December:
            today_t = today_n.replace(month=today_n.month + 1, day=1, hour=hour, minute=0, second=0, microsecond=0)
        except ValueError:
            # Only time it will go there is on December 30th:
            today_t = today_n.replace(year=today_n.year + 1, month=1, day=1, hour=hour, minute=0, second=0,
                                      microsecond=0)
    return int((today_t - today_n).seconds + 1)


def split_list(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]


def is_owner(user_id: str):
    return user_id == hidden.owner_id()


def check_folder(folder_name: str):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)


def check_file(file_name: str):
    if not os.path.exists(file_name):
        open(file_name, 'w').close()
