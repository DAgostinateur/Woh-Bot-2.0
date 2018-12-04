import discord
import os
import asyncio
import random

import util
import command_template


class Play(command_template.Command):
    crab_rave = "D:/Desktop files/Music/Crab Rave Mother 3.mp3"
    deltarune_folder = "D:/Desktop files/Music/HighQualityVideoGameRips/Toby Fox - DELTARUNE Chapter 1 OST"

    def __init__(self, client):
        super(Play, self).__init__(client)

        self.enabled = True
        self.perm_level = self.permission_everyone
        self.cmd_name = "play"
        self.arguments = "[song/playlist]"
        self.help_description = "'crab' plays the Crab Rave Mother 3 rip. 'deltarune' plays the entire OST. " \
                                "There might be a 0 to 4 second delay between songs."

        self.vc = None
        self.activated_in_channel = None
        self.player = None
        self.playlist_songs = None
        self.playlist_index = 0
        self.current_song = None

    async def disconnect_timer(self):
        while not self.parent_client.is_closed:
            if self.vc is not None:
                if self.player is not None:
                    if self.player.is_done():
                        if self.parent_client.music_repeat:
                            await self.make_player(self.current_song)
                        elif self.playlist_songs is not None:
                            pass
                            if len(self.playlist_songs) - 1 > self.playlist_index:
                                self.playlist_index += 1
                                await self.make_player(self.playlist_songs[self.playlist_index])
                            else:
                                await self.send_message_check(self.activated_in_channel, "Playlist ended.")
                                await self.vc.disconnect()
                                self.leave_vc()
                        else:
                            await self.vc.disconnect()
                            self.leave_vc()

            await asyncio.sleep(4)

    def leave_vc(self):
        self.vc = None
        self.activated_in_channel = None
        self.player = None
        self.playlist_songs = None
        self.playlist_index = 0
        self.current_song = None

    async def make_voice_client(self, message: discord.Message):
        self.vc = await self.parent_client.join_voice_channel(message.author.voice_channel)
        self.activated_in_channel = message.channel

    async def make_player(self, song):
        self.current_song = song
        self.player = self.vc.create_ffmpeg_player(song)
        self.player.volume = 0.3
        self.player.start()

    def set_playlist(self):
        self.playlist_songs = []
        for file in os.listdir(self.deltarune_folder):
            if util.is_music_file(os.path.join(self.deltarune_folder, file)):
                self.playlist_songs.append(os.path.join(self.deltarune_folder, file))
        random.shuffle(self.playlist_songs)

    async def command(self, message: discord.Message):
        if not self.execute_cmd(message):
            return

        song_name = self.rm_cmd(message)

        if message.author.voice.voice_channel is not None and len(self.parent_client.voice_clients) == 0:
            if song_name == "deltarune":
                self.set_playlist()
                await self.make_voice_client(message)
                await self.make_player(self.playlist_songs[self.playlist_index])
            elif song_name == 'crab':
                await self.make_voice_client(message)
                await self.make_player(self.crab_rave)
            else:
                await self.send_message_check(message.channel, self.help_description)
        else:
            if self.playlist_songs is None:
                await self.send_message_check(message.channel, "There's a song playing.")
            else:
                await self.send_message_check(message.channel, "There's a playlist playing.")
