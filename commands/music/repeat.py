import discord

import command_template


class Repeat(command_template.Command):
    def __init__(self, client):
        super(Repeat, self).__init__(client)

        self.enabled = True
        self.perm_level = self.permission_everyone
        self.cmd_name = "loop"
        self.arguments = ""
        self.help_description = "Loops the current song. There might be a 0 to 4 second delay between songs."

    async def command(self, message: discord.Message):
        if not self.execute_cmd(message):
            return

        self.parent_client.music_repeat = not self.parent_client.music_repeat
        if self.parent_client.music_repeat:
            await self.send_message_check(message.channel, "Current song now repeats.")
        else:
            await self.send_message_check(message.channel, "Current song no longer repeats.")
