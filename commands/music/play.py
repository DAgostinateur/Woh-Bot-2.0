import discord
import asyncio

import command_template


class Play(command_template.Command):
    temp_file_name = "D:/Desktop files/Music/Crab Rave Mother 3.mp3"

    def __init__(self, client):
        super(Play, self).__init__(client)

        self.enabled = True
        self.perm_level = self.permission_everyone
        self.cmd_name = "play"
        self.arguments = ""
        self.help_description = "TEMPORARY. Plays the Crab Rave Mother 3 rip."

        self.player = None
        self.vc = None

    async def disconnect_timer(self):
        while not self.parent_client.is_closed:
            if self.vc is not None:
                if self.player is not None:
                    if self.player.is_done():
                        self.player = None
                        await self.vc.disconnect()

            await asyncio.sleep(5)

    async def make_player(self, message: discord.Message):
        self.vc = await self.parent_client.join_voice_channel(message.author.voice_channel)
        self.player = self.vc.create_ffmpeg_player(self.temp_file_name)
        self.player.volume = 0.6
        self.player.start()

    async def command(self, message: discord.Message):
        if not self.execute_cmd(message):
            return

        if message.author.voice.voice_channel is not None and len(self.parent_client.voice_clients) == 0:
            await self.make_player(message)
