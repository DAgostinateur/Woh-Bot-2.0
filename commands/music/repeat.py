import discord

import command_template


class Repeat(command_template.Command):
    def __init__(self, client):
        super(Repeat, self).__init__(client)

        self.enabled = True
        self.perm_level = self.permission_everyone
        self.cmd_name = "loop"
        self.arguments = ""
        self.help_description = "Loops the current song."

    async def command(self, message: discord.Message):
        if not self.execute_cmd(message):
            return

        text_output = self.parent_client.music_handler.repeat()
        await self.send_message_check(message.channel, text_output)
