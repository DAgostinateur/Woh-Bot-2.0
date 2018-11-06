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
        self.arguments = "(-d)"
        self.help_description = "Lists the birthdays of everyone in this server." \
                                " Adding '-d' sorts by date instead of closest"

    @staticmethod
    def sort_by_closest(bd_list: list):
        return sorted([x for x in bd_list if x.get_datetime_date() > datetime.date.today()],
                      key=lambda s: s.get_datetime_date() - datetime.date.today())

    @staticmethod
    def sort_by_date(bd_list: list):
        return sorted(bd_list, key=lambda s: s.get_datetime_date_no_adjustment())

    def get_birthday_inlines(self, message: discord.Message, sort_method):
        inlines = []
        for user_bd in sort_method(self.parent_client.birthday_handler.user_birthdays):
            member = message.server.get_member(user_bd.user_id)
            if user_bd.server_id == message.server.id and member is not None:
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

    async def command(self, message: discord.Message):
        if not self.execute_cmd(message):
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
