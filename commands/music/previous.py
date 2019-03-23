import discord

import util
import command_template


class Previous(command_template.Command):
    def __init__(self, client):
        super(Previous, self).__init__(client)

        self.enabled = True
        self.perm_level = self.permission_levels["everyone"]
        self.cmd_name = "previous"
        self.arguments = "(number)"
        self.help_description = "Plays the previous song in a playlist. Adding a number goes back x songs"

    async def command(self, message: discord.Message):
        if not self.execute_cmd(message):
            return

        back = self.rm_cmd(message)

        if len(back) != 0:
            if util.is_int(back):
                if int(back) > 0:
                    back = int(back)
                else:
                    back = 1
        else:
            back = 1

        if self.parent_client.music_handler.is_in_vc(message):
            if self.parent_client.music_handler.playlist_songs is not None:
                await self.parent_client.music_handler.previous(back)
                await self.send_message_check(message.channel, "Previous song!")
            else:
                await self.send_message_check(message.channel, "There's no playlist on.")
        else:
            await self.send_message_check(message.channel, "There's nothing playing.")
