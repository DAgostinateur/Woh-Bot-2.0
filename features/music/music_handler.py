import discord
import os
import asyncio
import random

import util
import features.music.song


class MusicHandler(object):
    default_volume = 0.25

    crab_rave = "D:/Desktop files/Music/Crab Rave Mother 3.mp3"
    deltarune_folder = "D:/Desktop files/Music/HighQualityVideoGameRips/Toby Fox - DELTARUNE Chapter 1 OST"
    hqplaylist_folder = "D:/Desktop files/Music/HighQualityVideoGameRips"

    def __init__(self, client):
        self.parent_client = client

        self.music_repeat = False
        self.volume = self.default_volume

        # Only one VoiceClient will be available to this bot
        self.vc = None  # Client's VoiceClient
        self.activated_in_channel = None  # Channel
        self.player = None

        self.playlist_songs = None
        self.playlist_index = 0
        self.current_song = None  # Will be the Song class

    async def send_message_check(self, channel: discord.Channel, text):
        try:
            await self.parent_client.send_message(channel, text)
        except discord.NotFound:
            print("Channel '{}' probably doesn't exist.".format(channel.id))
        except discord.Forbidden:
            print("Client doesn't have permission to send a message in '{}'.".format(channel.id))

    async def disconnect_timer(self):
        while not self.parent_client.is_closed:
            await asyncio.sleep(4)
            if self.vc is None:
                continue

            if self.player is None:
                continue

            if self.player.is_done():
                if self.music_repeat:
                    await self.make_player(self.current_song.file_location)
                elif self.playlist_songs is not None:
                    if len(self.playlist_songs) - 1 > self.playlist_index:
                        await self.next()
                    else:
                        await self.send_message_check(self.activated_in_channel, "Playlist ended.")
                        await self.leave_vc()
                else:
                    await self.leave_vc()

    def is_in_vc(self, message: discord.Message):
        # Both the person that did the command and the bot
        return not (message.author.voice.voice_channel is not None and len(self.parent_client.voice_clients) == 0)

    def reset(self):
        self.vc = None
        self.activated_in_channel = None
        self.player = None

        self.playlist_songs = None
        self.playlist_index = 0
        self.current_song = None

    async def leave_vc(self):
        await self.vc.disconnect()
        self.reset()

    async def make_voice_client(self, message: discord.Message):
        self.vc = await self.parent_client.join_voice_channel(message.author.voice_channel)
        self.activated_in_channel = message.channel

    async def make_player(self, song):
        self.current_song = song
        self.player = self.vc.create_ffmpeg_player(self.current_song.file_location)
        self.player.volume = self.volume
        self.player.start()

    async def play(self, message: discord.Message, music_option):
        # Return is the text output to send in chat
        # Check with is_in_vc before coming here
        if music_option == "deltarune":
            await self.send_message_check(message.channel, "Loading playlist.")
            self.set_playlist(self.deltarune_folder)
            await self.make_voice_client(message)
            await self.make_player(self.playlist_songs[self.playlist_index])
        elif music_option == "hqplaylist":
            await self.send_message_check(message.channel, "Loading playlist.")
            self.set_multi_folder_playlist(self.hqplaylist_folder)
            await self.make_voice_client(message)
            await self.make_player(self.playlist_songs[self.playlist_index])
        elif music_option == 'crab':
            await self.send_message_check(message.channel, "Loading song.")
            await self.make_voice_client(message)
            await self.make_player(features.music.song.Song(self.crab_rave))
        else:
            await self.send_message_check(message.channel,
                                          "'crab' plays the Crab Rave Mother 3 rip. 'deltarune' plays the entire OST. "
                                          "'hqplaylist' plays D'Agostinateur Woh's entire playlist.")

    def resume(self):
        if self.player is not None:
            if not self.player.is_playing():
                self.player.resume()
                return "Resumed."
            else:
                return "It's already playing."
        else:
            return "Nothing to resume."

    def pause(self):
        if self.player is not None:
            if self.player.is_playing():
                self.player.pause()
                return "Paused."
            else:
                return "It's already paused."
        else:
            return "Nothing to pause."

    async def next(self):
        self.player.stop()
        if self.playlist_index > len(self.playlist_songs) - 1:
            await self.send_message_check(self.activated_in_channel, "Playlist ended.")
            await self.leave_vc()
            return
        self.playlist_index += 1
        await self.make_player(self.playlist_songs[self.playlist_index])

    async def previous(self):
        self.player.stop()
        self.playlist_index -= 1
        if 0 > self.playlist_index:
            self.playlist_index = 0
        await self.make_player(self.playlist_songs[self.playlist_index])

    def set_volume(self, vol):
        self.volume = vol
        if self.player is not None:
            self.player.volume = vol

        return "Volume set to {}.".format(int(vol * 100))

    def repeat(self):
        self.music_repeat = not self.music_repeat
        if self.music_repeat:
            return "Loop enabled."
        else:
            return "Loop disabled."

    def player_info(self):
        total_songs = 0
        position = 0

        if self.playlist_songs is None:
            if self.current_song is not None:
                total_songs = 1
                position = 1
        else:
            total_songs = len(self.playlist_songs)
            position = self.playlist_index + 1

        return "Will loop: {}\nTotal Songs: {}\nCurrent position: {}".format(self.music_repeat, total_songs, position)

    def song_info(self):
        title = "N/A"
        artist = "N/A"
        duration = "N/A"

        if self.current_song is not None:
            title = self.current_song.get_info(features.music.song.Song.TITLE)
            artist = self.current_song.get_info(features.music.song.Song.ARTIST)
            duration = util.format_duration(self.current_song.get_duration())

        return "\nTitle: {}\nArtist: {}\nDuration: {}".format(title, artist, duration)

    def set_multi_folder_playlist(self, double_layer_folder):
        self.playlist_songs = []
        for folder in os.listdir(double_layer_folder):
            if os.path.isdir(os.path.join(double_layer_folder, folder)):
                for file in os.listdir(os.path.join(double_layer_folder, folder)):
                    if util.is_music_file(os.path.join(double_layer_folder, folder, file)):
                        song = features.music.song.Song(os.path.join(double_layer_folder, folder, file))
                        self.playlist_songs.append(song)
        random.shuffle(self.playlist_songs)

    def set_playlist(self, simple_folder):
        self.playlist_songs = []
        for file in os.listdir(simple_folder):
            if util.is_music_file(os.path.join(simple_folder, file)):
                song = features.music.song.Song(os.path.join(simple_folder, file))
                self.playlist_songs.append(song)
        random.shuffle(self.playlist_songs)
