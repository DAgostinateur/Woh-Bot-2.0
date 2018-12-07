import discord

import command_template


class NowPlaying(command_template.Command):
    def __init__(self, client):
        super(NowPlaying, self).__init__(client)

        self.enabled = True
        self.perm_level = self.permission_everyone
        self.cmd_name = "np"
        self.arguments = ""
        self.help_description = "Displays info about the currently playing song."

    async def command(self, message: discord.Message):
        if not self.execute_cmd(message):
            return

        await self.send_message_check(message.channel, self.parent_client.music_handler.song_info())
