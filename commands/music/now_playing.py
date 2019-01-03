import discord

import command_template


class NowPlaying(command_template.Command):
    def __init__(self, client):
        super(NowPlaying, self).__init__(client)

        self.enabled = True
        self.perm_level = self.permission_levels["everyone"]
        self.cmd_name = "np"
        self.arguments = ""
        self.help_description = "Displays info about the currently playing song."

    async def command(self, message: discord.Message):
        if not self.execute_cmd(message):
            return

        if self.parent_client.music_handler.is_in_vc(message):
            await self.parent_client.send_message(message.channel,
                                                  embed=self.parent_client.music_handler.get_now_playing_embed())
        else:
            await self.send_message_check(message.channel, "There's nothing playing.")
