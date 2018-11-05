import discord
import datetime

import command_template
import util


class ListUserBD(command_template.Command):
    def __init__(self, client):
        super(ListUserBD, self).__init__(client)

        self.enabled = True
        self.perm_level = self.permission_admin
        self.cmd_name = "listuserbd"
        self.arguments = ""
        self.help_description = "Lists the birthdays of everyone in this server."

    @staticmethod
    def sort_bd_list(bd_list: list):
        return sorted([x for x in bd_list if x.get_datetime_date() > datetime.date.today()],
                      key=lambda s: s.get_datetime_date() - datetime.date.today())

    def get_birthday_inlines(self, message: discord.Message):
        inlines = []
        for user_bd in self.sort_bd_list(self.parent_client.birthday_handler.user_birthdays):
            member = message.server.get_member(user_bd.user_id)
            if user_bd.server_id == message.server.id and member is not None:
                inlines.append({"name": member.name, "inline": "true",
                                "value": "{} {}".format(user_bd.get_readable_month(), user_bd.get_readable_day())})
        return inlines

    def get_full_birthday_embeds(self, message: discord.Message):
        embeds = []

        if len(self.get_birthday_inlines(message)) == 0:
            embed = discord.Embed(colour=self.colour_birthday, description="No one in the list!")
            embed.set_thumbnail(url="https://emojipedia-us.s3.dualstack.us-west-1."
                                    "amazonaws.com/thumbs/120/twitter/154/birthday-cake_1f382.png")
            embed.set_author(name="Birthday List",
                             icon_url="https://emojipedia-us.s3.dualstack.us-west-1."
                                      "amazonaws.com/thumbs/120/twitter/154/confetti-ball_1f38a.png")
            embeds.append(embed)

        for fields in util.split_list(self.get_birthday_inlines(message), 25):
            embed = discord.Embed(colour=self.colour_birthday)
            embed.set_thumbnail(url="https://emojipedia-us.s3.dualstack.us-west-1."
                                    "amazonaws.com/thumbs/120/twitter/154/birthday-cake_1f382.png")
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

        try:
            for embed in self.get_full_birthday_embeds(message):
                await self.parent_client.send_message(message.channel, embed=embed)
        except discord.Forbidden:
            print("Client doesn't have permission to send a message in '{}'.".format(message.channel.id))
