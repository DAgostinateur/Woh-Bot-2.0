import asyncio
import os
import json
import discord
import datetime
import pytz

import util
from features.birthday import user_birthday, channel_birthday, message_birthday


class BirthdayHandler(object):
    user_birthday_file = "data/user_birthday.json"
    channel_birthday_file = "data/channel_birthday.json"
    message_birthday_file = "data/message_birthday.json"

    json_user_id = "user_id"
    json_birthday_date = "birthday_date"
    json_channel_id = "channel_id"
    json_server_id = "server_id"
    json_birthday_message = "birthday_message"

    def __init__(self, client):
        self.parent_client = client

        self.user_birthdays = self.get_user_birthdays()
        self.channel_birthdays = self.get_channel_birthdays()
        self.message_birthdays = self.get_message_birthdays()

    def _write_to_user_file(self):
        info_dicts = [
            {self.json_user_id: x.user_id, self.json_birthday_date: x.birthday_date, self.json_server_id: x.server_id}
            for x in self.user_birthdays]
        json_string = json.dumps(info_dicts, indent=4, separators=(',', ' : '))
        with open(self.user_birthday_file, 'w') as file:
            file.write(json_string)

    def _write_to_channel_file(self):
        info_dicts = [{self.json_channel_id: x.channel_id, self.json_server_id: x.server_id} for x in
                      self.channel_birthdays]
        json_string = json.dumps(info_dicts, indent=4, separators=(',', ' : '))
        with open(self.channel_birthday_file, 'w') as file:
            file.write(json_string)

    def _write_to_message_file(self):
        info_dicts = [{self.json_server_id: x.server_id, self.json_birthday_message: x.birthday_message} for x in
                      self.message_birthdays]
        json_string = json.dumps(info_dicts, indent=4, separators=(',', ' : '))
        with open(self.message_birthday_file, 'w') as file:
            file.write(json_string)

    async def send_birthday_message(self, channel_id, user_id, bd_message, date):
        user = await self.parent_client.get_user_info(user_id)
        author_name = "Happy Birthday {}".format(user.name)

        try:
            embed = util.make_embed(colour=util.colour_birthday, description=bd_message, author_name=author_name,
                                    author_icon_url=util.image_confetti, thumbnail_url=user.avatar_url,
                                    footer_text=date)
            await self.parent_client.send_message(self.parent_client.get_channel(channel_id), content=user.mention,
                                                  embed=embed)
        except discord.NotFound:
            print("Channel '{}' probably doesn't exist.".format(channel_id))
        except discord.Forbidden:
            print("Client doesn't have permission to send a message in '{}'.".format(channel_id))

    async def happy_birthday_checker(self):
        mm_dd = str(datetime.datetime.now(pytz.timezone('EST')))[5:10]
        for channel_bd in self.channel_birthdays:
            server = self.parent_client.get_server(channel_bd.server_id)
            if server is None:
                continue

            message_bd = self.get_message_bd(server.id)
            if message_bd is not None:
                message_bd = message_bd.birthday_message
            else:
                message_bd = message_birthday.MessageBirthday.default_message

            for user_bd in self.user_birthdays:
                if server.get_member(user_bd.user_id) is None:
                    continue

                if mm_dd == user_bd.birthday_date and channel_bd.server_id == user_bd.server_id:
                    await self.send_birthday_message(channel_bd.channel_id, user_bd.user_id, message_bd,
                                                     user_bd.get_readable_date())

    async def birthday_timer(self):
        await self.parent_client.wait_until_ready()
        while not self.parent_client.is_closed:
            await asyncio.sleep(util.get_next_day_delta(self.parent_client.settings.get_default_notification_time()))
            await self.happy_birthday_checker()

    def check_birthday_lists(self):
        for channel_bd in self.channel_birthdays:
            server = self.parent_client.get_server(channel_bd.server_id)
            if server is None:
                message_bd = self.get_message_bd(channel_bd.server_id)
                if message_bd is not None:
                    self.remove_message_birthday(channel_bd.server_id)

                self.remove_channel_birthday(channel_bd.server_id)
            else:
                for user_bd in self.user_birthdays:
                    member = server.get_member(user_bd.user_id)
                    if member is None and user_bd.server_id == server.id:
                        self.remove_user_birthday(user_bd.user_id, user_bd.server_id)

    def get_birthday_count(self, server: discord.Server):
        count = 0
        for user_bd in self.user_birthdays:
            if user_bd.server_id == server.id and server.get_member(user_bd.user_id) is not None:
                count += 1
        return count

    def get_user_bd(self, user_id, server_id):
        """Returns a UserBirthday with a user id and a server id

        :param user_id:
        :param server_id:
        :return: UserBirthday
        """
        for user_bd in self.user_birthdays:
            if user_bd.user_id == user_id and server_id == user_bd.server_id:
                return user_bd
        return None

    def get_channel_bd(self, server_id):
        """Returns a ChannelBirthday with a server id

        :param server_id:
        :return: ChannelBirthday
        """
        for channel_bd in self.channel_birthdays:
            if channel_bd.server_id == server_id:
                return channel_bd
        return None

    def get_message_bd(self, server_id):
        """Returns a MessageBirthday with a server id

        :param server_id:
        :return: MessageBirthday
        """
        for message_bd in self.message_birthdays:
            if message_bd.server_id == server_id:
                return message_bd
        return None

    def get_user_birthdays(self):
        if not os.path.exists(self.user_birthday_file):
            util.check_file(self.user_birthday_file)
            return []

        with open(self.user_birthday_file, 'r') as file:
            if os.stat(self.user_birthday_file).st_size == 0:
                return []

            user_birthday_list = []
            for d in json.load(file):
                try:
                    user_birthday_list.append(
                        user_birthday.UserBirthday(d[self.json_user_id], d[self.json_birthday_date],
                                                   d[self.json_server_id]))
                except KeyError:
                    print("user_id or birthday_date doesnt exist: {}".format(d))

            return user_birthday_list

    def save_user_birthday(self, user_id, birthday_date, server_id):
        self.user_birthdays.append(user_birthday.UserBirthday(user_id, birthday_date, server_id))
        print("SUCCEEDED to add user birthday.")
        self._write_to_user_file()

    def remove_user_birthday(self, user_id, server_id):
        try:
            self.user_birthdays.remove(self.get_user_bd(user_id, server_id))
        except ValueError:
            print("FAILED to remove user birthday.")
            return

        self._write_to_user_file()

        print("SUCCEEDED to remove user birthday.")

    def get_channel_birthdays(self):
        if not os.path.exists(self.channel_birthday_file):
            util.check_file(self.channel_birthday_file)
            return []

        with open(self.channel_birthday_file, 'r') as file:
            if os.stat(self.channel_birthday_file).st_size == 0:
                return []

            channel_birthday_list = []
            for d in json.load(file):
                try:
                    channel_birthday_list.append(
                        channel_birthday.ChannelBirthday(d[self.json_channel_id], d[self.json_server_id]))
                except KeyError:
                    print("channel_id or server_id doesnt exist: {}".format(d))

            return channel_birthday_list

    def save_channel_birthday(self, channel_id, server_id):
        self.channel_birthdays.append(channel_birthday.ChannelBirthday(channel_id, server_id))
        print("SUCCEEDED to add channel birthday.")
        self._write_to_channel_file()

    def remove_channel_birthday(self, server_id):
        try:
            self.channel_birthdays.remove(self.get_channel_bd(server_id))
        except (ValueError, AttributeError):
            print("FAILED to remove channel birthday.")
            return

        self._write_to_channel_file()

        print("SUCCEEDED to remove channel birthday.")

    def get_message_birthdays(self):
        if not os.path.exists(self.message_birthday_file):
            util.check_file(self.message_birthday_file)
            return []

        with open(self.message_birthday_file, 'r') as file:
            if os.stat(self.message_birthday_file).st_size == 0:
                return []

            message_birthday_list = []
            for d in json.load(file):
                try:
                    message_birthday_list.append(
                        message_birthday.MessageBirthday(d[self.json_server_id], d[self.json_birthday_message]))
                except KeyError:
                    print("server_id or birthday_message doesnt exist: {}".format(d))

            return message_birthday_list

    def save_message_birthday(self, server_id, birthday_message):
        self.message_birthdays.append(message_birthday.MessageBirthday(server_id, birthday_message))
        print("SUCCEEDED to add message birthday.")
        self._write_to_message_file()

    def remove_message_birthday(self, server_id):
        try:
            self.message_birthdays.remove(self.get_message_bd(server_id))
        except (ValueError, AttributeError):
            print("FAILED to remove message birthday.")
            return

        self._write_to_message_file()

        print("SUCCEEDED to remove message birthday.")
