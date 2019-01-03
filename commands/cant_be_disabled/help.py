import discord

import util
import command_template


class Help(command_template.Command):
    max_fields = 25

    def __init__(self, handler):
        super(Help, self).__init__(handler)

        self.enabled = True  # Should never change
        self.perm_level = self.permission_levels["everyone"]
        self.cmd_name = "help"
        self.arguments = "(command)"
        self.help_description = "Shows every available command and their description, can specify a command. " \
                                "This command can not be disabled."

    def get_full_cmd_embeds(self):
        embeds = []

        description = "Prefix: {}\nCommand names are not case sensitive.\n" \
                      "'()' means optional.\n'(-letter/letter)' means optional options, " \
                      "can be combined if specified, slash isn't included in the command.\n" \
                      "'[]' means required.".format(self.parent_client.prefix)

        for fields in util.split_list(self.handler.get_cmd_inlines(), 25):
            embeds.append(
                util.make_embed(colour=util.colour_royal_purple, description=description, author_name="Help",
                                author_icon_url=util.image_question_mark, fields=fields))

        return embeds

    def get_cmd_embed(self):
        description = "\nUse: {}{} {}\n\n{}".format(self.parent_client.prefix, self.cmd_name, self.arguments,
                                                    self.help_description)

        return util.make_embed(colour=util.colour_royal_purple, description=description,
                               author_name="Command Name: {}".format(self.cmd_name))

    async def command(self, message: discord.Message):
        if not self.execute_cmd(message):
            return

        command = self.handler.get_cmd(self.rm_cmd(message).lower())
        try:
            if command is None:
                for embed in self.get_full_cmd_embeds():
                    await self.parent_client.send_message(message.author, embed=embed)
            else:
                await self.parent_client.send_message(message.channel, embed=command.get_help_embedded())
        except discord.Forbidden:
            print("Client doesn't have permission to send a message in '{}'.".format(message.channel.id))
