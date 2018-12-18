import discord
import datetime

import command_template
import util


class ListUserBD(command_template.Command):
    def __init__(self, client):
        super(ListUserBD, self).__init__(client)

        self.enabled = True
        self.perm_level = self.permission_levels["everyone"]
        self.cmd_name = "listuserbd"
        self.arguments = "(-a/c/d)"
        self.option_letters = "acd"
        self.help_description = "Lists the birthdays of everyone in this server by closest by default. " \
                                "'-d' sorts by date instead. '-a' displays astrological sign. " \
                                "'c' will display the birthday count. Option 'acd' can be combined."

    @staticmethod
    def sort_by_closest(bd_list: list):
        return sorted([x for x in bd_list if x.get_datetime_date() >= datetime.date.today()],
                      key=lambda s: s.get_datetime_date() - datetime.date.today())

    @staticmethod
    def sort_by_date(bd_list: list):
        return sorted(bd_list, key=lambda s: s.get_datetime_date_no_adjustment())

    @staticmethod
    def make_field(member, value):
        return {"name": member.name, "inline": "true", "value": value}

    def get_count_description(self, message: discord.Message):
        return "There's {} members in the birthday list in this server".format(
            self.parent_client.birthday_handler.get_birthday_count(message.server))

    def add_astrological_signs(self, member, user_bd):
        return self.make_field(member, "{} {}  - {}".format(user_bd.get_readable_month(),
                                                            user_bd.get_readable_day(),
                                                            user_bd.get_astrological_sign()))

    def get_birthday_inlines(self, message: discord.Message):
        inlines = []
        sorted_bd_list = []

        if self.has_wanted_argument(message, "d"):
            for user_bd in self.sort_by_date(self.parent_client.birthday_handler.user_birthdays):
                sorted_bd_list.append(user_bd)
        else:
            for user_bd in self.sort_by_closest(self.parent_client.birthday_handler.user_birthdays):
                sorted_bd_list.append(user_bd)

        if self.has_wanted_argument(message, "a"):
            for user_bd in sorted_bd_list:
                member = message.server.get_member(user_bd.user_id)
                if user_bd.server_id == message.server.id and member is not None:
                    inlines.append(self.add_astrological_signs(member, user_bd))
        else:
            for user_bd in sorted_bd_list:
                member = message.server.get_member(user_bd.user_id)
                if user_bd.server_id == message.server.id and member is not None:
                    inlines.append(self.make_field(member, "{} {}".format(user_bd.get_readable_month(),
                                                                          user_bd.get_readable_day())))

        return inlines

    async def get_full_birthday_embeds(self, message: discord.Message):
        embeds = []
        description = ""

        if len(self.get_birthday_inlines(message)) == 0:
            embeds.append(
                util.make_embed(util.colour_birthday, "No one is in this list!",
                                "Birthday List", util.image_confetti, None, None, None))

        if self.has_wanted_argument(message, "c"):
            description = self.get_count_description(message)

        for fields in util.split_list(self.get_birthday_inlines(message), 25):
            embeds.append(
                util.make_embed(util.colour_birthday, description, "Birthday List", util.image_confetti, None, None,
                                fields))

        return embeds

    async def command(self, message: discord.Message):
        if not self.execute_cmd(message):
            return

        try:
            for embed in await self.get_full_birthday_embeds(message):
                await self.parent_client.send_message(message.channel, embed=embed)
        except discord.Forbidden:
            print("Client doesn't have permission to send a message in '{}'.".format(message.channel.id))
