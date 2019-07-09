import discord

import command_template


class Play(command_template.Command):
    def __init__(self, client):
        super(Play, self).__init__(client)

        self.enabled = True
        self.perm_level = self.permission_levels["everyone"]
        self.cmd_name = "play"
        self.arguments = "[song/playlist]"
        self.help_description = "'deltarune' plays the entire OST. " \
                                "'hqplaylist' plays D'Agostinatrice Woh's entire playlist." \
                                "There might be a 0 (not including 0 Morg) to 4 second delay between songs."

    async def command(self, message: discord.Message):
        if not self.execute_cmd(message):
            return

        music_option = self.rm_cmd(message)

        if not self.parent_client.music_handler.is_in_vc(message):
            await self.parent_client.music_handler.play(message, music_option)
        else:
            if self.parent_client.music_handler.playlist_songs is None:
                await self.send_message_check(message.channel, "You have to join the VC to use this command.")
            else:
                await self.send_message_check(message.channel, "There's a playlist playing.")
