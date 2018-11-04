import discord

import util
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

    def get_full_cmd_embeds(self):
        embeds = []

        title = "Commands:"
        description = "Prefix: {}\n'()' means optional,\n'[]' means required".format(self.parent_client.prefix)

        for fields in util.split_list(self.handler.get_cmd_inlines(), 25):
            embed = discord.Embed(title=title, description=description, colour=self.colour_royal_purple)
            embed.set_author(name="Help",
                             icon_url="https://emojipedia-us.s3.dualstack.us-west-1."
                                      "amazonaws.com/thumbs/120/twitter/154/white-question-mark-ornament_2754.png")
            for field in fields:
                embed.add_field(name=field["name"], value=field["value"])

            embeds.append(embed)

        return embeds

    def get_cmd_embed(self):
        title = "Command Name: {}".format(self.cmd_name)
        description = "\nUse: {}{} {}\n\n{}".format(self.parent_client.prefix, self.cmd_name,
                                                    self.arguments, self.help_description)
        return discord.Embed(title=title, description=description, colour=self.colour_royal_purple)

    async def command(self, message: discord.Message):
        if not self.execute_cmd(message):
            return

        command = self.handler.get_cmd(self.rm_cmd(message))
        try:
            if command is None:
                for embed in self.get_full_cmd_embeds():
                    await self.parent_client.send_message(message.channel, embed=embed)
            else:
                await self.parent_client.send_message(message.channel, embed=command.get_help_embedded())
        except discord.Forbidden:
            print("Client doesn't have permission to send a message in '{}'.".format(message.channel.id))
