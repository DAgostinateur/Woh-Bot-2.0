import discord

import command_template


class PlayerInfo(command_template.Command):
    def __init__(self, client):
        super(PlayerInfo, self).__init__(client)

        self.enabled = True
        self.perm_level = self.permission_everyone
        self.cmd_name = "playerinfo"
        self.arguments = ""
        self.help_description = "Displays info about the music player."

    async def command(self, message: discord.Message):
        if not self.execute_cmd(message):
            return

        await self.send_message_check(message.channel, self.parent_client.music_handler.player_info())
