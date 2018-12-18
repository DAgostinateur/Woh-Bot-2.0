import discord

import command_template


class Next(command_template.Command):
    def __init__(self, client):
        super(Next, self).__init__(client)

        self.enabled = True
        self.perm_level = self.permission_levels["everyone"]
        self.cmd_name = "next"
        self.arguments = ""
        self.help_description = "Plays the next song in a playlist."

    async def command(self, message: discord.Message):
        if not self.execute_cmd(message):
            return

        if self.parent_client.music_handler.is_in_vc(message):
            if self.parent_client.music_handler.playlist_songs is not None:
                await self.parent_client.music_handler.next()
                await self.send_message_check(message.channel, "Next song.")
            else:
                await self.send_message_check(message.channel, "There's no playlist on.")
        else:
            await self.send_message_check(message.channel, "There's nothing playing.")
