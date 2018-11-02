import discord

import command_template


class Help(command_template.Command):
    max_fields = 25

    def __init__(self, handler):
        super(Help, self).__init__(handler)

        self.enabled = True  # Should never change
        self.perm_level = self.permission_everyone
        self.cmd_name = "help"
        self.arguments = "(command)"
        self.help_description = "Shows every available command and their description, can specify a command. " \
                                "This command can not be disabled."

    def get_full_embeds(self):
        title = "Commands:"
        description = "Prefix: {}\n'()' means optional,\n'[]' means required".format(self.parent_client.prefix)
        fields = self.handler.get_embed_inlines()

        embed = discord.Embed(title=title, description=description, colour=self.colour_royal_purple)
        embed.set_author(name="Help", icon_url="https://cdn.discordapp.com/emojis/492159765745500160.png?v=1")
        # embeds = []
        for field in fields:
            embed.add_field(name=field["name"], value=field["value"])
            # if len(embed.fields) >= 25:

        return embed

    def get_cmd_embed(self):
        title = "Command Name: {}".format(self.cmd_name)
        description = "\nUse: {}{} {}\n\n{}".format(self.parent_client.prefix, self.cmd_name,
                                                    self.arguments, self.help_description)
        return discord.Embed(title=title, description=description, colour=self.colour_royal_purple)

    async def command(self, message: discord.Message):
        if not self.execute_cmd(message):
            return

        command = self.handler.get_cmd(self.rm_cmd(message))
        if command is None:
            await self.parent_client.send_message(message.channel, embed=self.get_full_embeds())
        else:
            await self.parent_client.send_message(message.channel, embed=command.get_help_embedded())
