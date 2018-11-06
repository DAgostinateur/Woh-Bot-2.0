import discord
import datetime

import command_template
import util


class ListUserBD(command_template.Command):
    def __init__(self, client):
        super(ListUserBD, self).__init__(client)

        self.enabled = True
        self.perm_level = self.permission_everyone
        self.cmd_name = "listuserbd"
        self.arguments = "(-d/a/c)"
        self.help_description = "Lists the birthdays of everyone in this server by closest by default. " \
                                "Adding '-d' sorts by date instead. Adding '-a' also displays astrological sign. " \
                                "'c' will display the birthday count. Option 'ad' can be combined"

    @staticmethod
    def sort_by_closest(bd_list: list):
        return sorted([x for x in bd_list if x.get_datetime_date() > datetime.date.today()],
                      key=lambda s: s.get_datetime_date() - datetime.date.today())

    @staticmethod
    def sort_by_date(bd_list: list):
        return sorted(bd_list, key=lambda s: s.get_datetime_date_no_adjustment())

    def get_birthday_count(self, message):
        count = 0
        for user_bd in self.parent_client.birthday_handler.user_birthdays:
            if user_bd.server_id == message.server.id and message.server.get_member(user_bd.user_id) is not None:
                count += 1
        return count

    def get_birthday_inlines(self, message: discord.Message, sort_method):
        inlines = []
        for user_bd in sort_method(self.parent_client.birthday_handler.user_birthdays):
            member = message.server.get_member(user_bd.user_id)
            if user_bd.server_id == message.server.id and member is not None:
                if "-da" in message.content or "-ad" in message.content or "-a" in message.content:
                    inlines.append({"name": member.name, "inline": "true",
                                    "value": "{} {}  - {}".format(user_bd.get_readable_month(),
                                                                  user_bd.get_readable_day(),
                                                                  user_bd.get_astrological_sign())})
                else:
                    inlines.append({"name": member.name, "inline": "true",
                                    "value": "{} {}".format(user_bd.get_readable_month(), user_bd.get_readable_day())})
        return inlines

    def get_full_birthday_embeds(self, message: discord.Message, sort_method):
        embeds = []

        if len(self.get_birthday_inlines(message, sort_method)) == 0:
            embed = discord.Embed(colour=self.colour_birthday, description="No one in the list!")
            embed.set_author(name="Birthday List",
                             icon_url="https://emojipedia-us.s3.dualstack.us-west-1."
                                      "amazonaws.com/thumbs/120/twitter/154/confetti-ball_1f38a.png")
            embeds.append(embed)

        for fields in util.split_list(self.get_birthday_inlines(message, sort_method), 25):
            embed = discord.Embed(colour=self.colour_birthday)
            embed.set_author(name="Birthday List",
                             icon_url="https://emojipedia-us.s3.dualstack.us-west-1."
                                      "amazonaws.com/thumbs/120/twitter/154/confetti-ball_1f38a.png")
            for field in fields:
                embed.add_field(name=field["name"], value=field["value"])

            embeds.append(embed)

        return embeds

    def get_birthday_count_embed(self, message):
        embed = discord.Embed(colour=self.colour_birthday,
                              description="There's {} members in the birthday list in this server".format(
                                  self.get_birthday_count(message)))
        embed.set_author(name="Birthday List",
                         icon_url="https://emojipedia-us.s3.dualstack.us-west-1."
                                  "amazonaws.com/thumbs/120/twitter/154/confetti-ball_1f38a.png")
        return embed

    async def command(self, message: discord.Message):
        if not self.execute_cmd(message):
            return

        if '-c' in message.content:
            try:
                await self.parent_client.send_message(message.channel, embed=self.get_birthday_count_embed(message))
            except discord.Forbidden:
                print("Client doesn't have permission to send a message in '{}'.".format(message.channel.id))

            return

        if '-d' in message.content:
            try:
                for embed in self.get_full_birthday_embeds(message, self.sort_by_date):
                    await self.parent_client.send_message(message.channel, embed=embed)
            except discord.Forbidden:
                print("Client doesn't have permission to send a message in '{}'.".format(message.channel.id))
        else:
            try:
                for embed in self.get_full_birthday_embeds(message, self.sort_by_closest):
                    await self.parent_client.send_message(message.channel, embed=embed)
            except discord.Forbidden:
                print("Client doesn't have permission to send a message in '{}'.".format(message.channel.id))
