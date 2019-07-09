import discord
import datetime
import os
import string

import hidden


colour_voice = 481716
colour_join = 4304663
colour_leave = 13114910
colour_musical = 6139885
colour_royal_purple = 7885225
colour_birthday = 16428082
colour_admin = 27476

image_uncategorized_ledger = "https://emojipedia-us.s3.dualstack.us-west-1." \
                             "amazonaws.com/thumbs/120/twitter/185/ledger_1f4d2.png"
image_birthday = "https://emojipedia-us.s3.dualstack.us-west-1." \
                 "amazonaws.com/thumbs/120/twitter/185/birthday-cake_1f382.png"
image_logging_keylock = "https://emojipedia-us.s3.dualstack.us-west-1." \
                        "amazonaws.com/thumbs/120/twitter/185/closed-lock-with-key_1f510.png"
image_nodisabling_info = "https://emojipedia-us.s3.dualstack.us-west-1." \
                         "amazonaws.com/thumbs/120/twitter/185/information-source_2139.png"
image_music_note = "https://emojipedia-us.s3.dualstack.us-west-1." \
                   "amazonaws.com/thumbs/120/twitter/154/multiple-musical-notes_1f3b6.png"
image_admin_lock = "https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/twitter/154/lock_1f512.png"

image_confetti = "https://emojipedia-us.s3.dualstack.us-west-1." \
                 "amazonaws.com/thumbs/120/twitter/154/confetti-ball_1f38a.png"
image_question_mark = "https://emojipedia-us.s3.dualstack.us-west-1." \
                      "amazonaws.com/thumbs/120/twitter/154/white-question-mark-ornament_2754.png"


def make_embed(description, author_name, author_icon_url=None, thumbnail_url=None, footer_text=None, fields=None,
               colour=colour_royal_purple):
    embed = discord.Embed(colour=colour, description=description)
    if author_icon_url is None:
        embed.set_author(name=author_name)
    else:
        embed.set_author(name=author_name,
                         icon_url=author_icon_url)

    if thumbnail_url is not None:
        embed.set_thumbnail(url=thumbnail_url)

    if footer_text is not None:
        embed.set_footer(text=footer_text)

    if fields is not None:
        for field in fields:
            embed.add_field(name=field["name"],
                            value=field["value"], inline=field["inline"])

    return embed


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
    today_n = datetime.datetime.now()
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


def format_duration(duration: float):
    """Formats the duration (milliseconds) to a human readable way.

    :param duration: Duration in milliseconds
    :return: Duration in HOURS:MINUTES:SECONDS format. Example: 01:05:10
    """
    m, s = divmod(duration / 1000, 60)
    h, m = divmod(m, 60)
    if h:
        return "{0}:{1:0>2}:{2:0>2}".format(str(int(h)).zfill(2),
                                            str(int(m)).zfill(2), str(int(s)).zfill(2))
    else:
        return "{0}:{1:0>2}".format(str(int(m)).zfill(2), str(int(s)).zfill(2))


def is_music_file(file: str):
    return os.path.isfile(file) and file.lower().endswith('.mp3')


def is_printable(s: str):
    return all(c in string.printable for c in s)


def is_int(text):
    try:
        int(text)
        return True
    except ValueError:
        return False
    except TypeError:
        return False


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
