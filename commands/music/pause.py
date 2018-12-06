import discord

import command_template


class Pause(command_template.Command):
    def __init__(self, client):
        super(Pause, self).__init__(client)

        self.enabled = True
        self.perm_level = self.permission_everyone
        self.cmd_name = "pause"
        self.arguments = ""
        self.help_description = "Pauses the song."

    async def command(self, message: discord.Message):
        if not self.execute_cmd(message):
            return

        if self.parent_client.music_handler.is_in_vc(message):
            text_output = self.parent_client.music_handler.pause()
            await self.send_message_check(message.channel, text_output)
