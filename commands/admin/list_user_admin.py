import discord

import command_template
import util


class ListUserAdmin(command_template.Command):
    def __init__(self, client):
        super(ListUserAdmin, self).__init__(client)

        self.enabled = True
        self.perm_level = self.permission_levels["admin"]
        self.cmd_name = "listuseradmin"
        self.arguments = "(-c)"
        self.option_letters = "c"
        self.help_description = "Lists everyone with admin power for this bot in this server. " \
                                "'c' will display the admin count."

    @staticmethod
    def make_field(member):
        return {"name": member.name, "inline": "true", "value": "User Id: {}".format(member.id)}

    def get_count_description(self, message: discord.Message):
        return "There's {} members in the admin list in this server".format(
            self.parent_client.admin_handler.get_admin_count(message.server))

    def get_admin_inlines(self, message: discord.Message):
        inlines = []

        for user_admin in self.parent_client.admin_handler.user_admins:
            member = message.server.get_member(user_admin.user_id)
            if user_admin.server_id == message.server.id and member is not None:
                inlines.append(self.make_field(member))

        return inlines

    async def get_full_birthday_embeds(self, message: discord.Message):
        embeds = []
        description = ""

        if len(self.get_admin_inlines(message)) == 0:
            embeds.append(
                util.make_embed(colour=util.colour_admin, description="No one is in this list!",
                                author_name="Admin List", author_icon_url=util.image_lock))

        if self.has_wanted_argument(message, "c"):
            description = self.get_count_description(message)

        for fields in util.split_list(self.get_admin_inlines(message), 25):
            embeds.append(
                util.make_embed(colour=util.colour_admin, description=description, author_name="Admin List",
                                author_icon_url=util.image_lock, fields=fields))

        return embeds

    async def command(self, message: discord.Message):
        if not self.execute_cmd(message):
            return

        try:
            for embed in await self.get_full_birthday_embeds(message):
                await self.parent_client.send_message(message.channel, embed=embed)
        except discord.Forbidden:
            print("Client doesn't have permission to send a message in '{}'.".format(message.channel.id))
