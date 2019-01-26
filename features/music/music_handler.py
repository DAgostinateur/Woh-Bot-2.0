import discord
import os
import asyncio
import random

import util
import features.music.song


class MusicHandler(object):
    music_folder = "data/music"
    queue_half_length = 5
    # Add music in the correct locations
    music_playlist_paths = {"hqplaylist": os.path.join(music_folder, "hqplaylist"),
                            "deltarune": os.path.join(music_folder, "deltarune"),
                            "playlisttest": os.path.join(music_folder, "castle_constellations")}

    def __init__(self, client):
        self.parent_client = client

        util.check_folder(self.music_folder)

        self.alone_counter = 0  # 1=4 seconds 150=600seconds=10minutes
        self.music_repeat = False
        self.volume = self.parent_client.settings.get_default_volume()

        # Only one VoiceClient will be available to this bot
        self.vc = None  # Client's VoiceClient
        self.activated_in_channel = None  # Channel
        self.player = None

        self.playlist_name = None
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

            if len(self.vc.channel.voice_members) <= 1:
                if self.alone_counter == 150:
                    self.alone_counter = 0
                    await self.leave_vc()
                    continue
                self.alone_counter += 1

            if not self.player.is_done():
                continue

            if self.music_repeat:
                await self.make_player(self.current_song)
            elif self.playlist_songs is not None:
                if len(self.playlist_songs) - 1 > self.playlist_index:
                    await self.next()
                else:
                    await self.send_message_check(self.activated_in_channel, "Playlist ended.")
                    await self.leave_vc()
            else:
                await self.send_message_check(self.activated_in_channel,
                                              "Nobody hsa been in this voice channel for 10 minutes, bi bye.")
                await self.leave_vc()

    def is_in_vc(self, message: discord.Message):
        # Both the person that did the command and the bot
        return not (message.author.voice.voice_channel is not None and len(self.parent_client.voice_clients) == 0)

    def reset(self):
        self.vc = None
        self.activated_in_channel = None
        self.player = None

        self.playlist_name = None
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
        # Check with is_in_vc before coming here
        try:
            # Should never be NoneType
            playlist = self.music_playlist_paths[music_option]
        except (KeyError, TypeError):
            await self.send_message_check(message.channel,
                                          "'deltarune' plays the entire OST. "
                                          "'hqplaylist' plays D'Agostinateur Woh's entire playlist.")
            return

        await self.send_message_check(message.channel, "Loading playlist.")
        util.check_folder(playlist)
        self.set_playlist(playlist)
        if len(self.playlist_songs) == 0:
            self.playlist_songs = None
            await self.send_message_check(message.channel, "Folder '{}' is empty.".format(playlist))
            return

        await self.make_voice_client(message)
        await self.make_player(self.playlist_songs[self.playlist_index])
        self.playlist_name = music_option

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
        if self.playlist_index >= len(self.playlist_songs) - 1:
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
        self.parent_client.settings.save_user_defaults(volume=vol)
        if self.player is not None:
            self.player.volume = vol

        return "Volume set to {}.".format(int(vol * 100))

    def repeat(self):
        self.music_repeat = not self.music_repeat
        if self.music_repeat:
            return "Loop enabled."
        else:
            return "Loop disabled."

    @staticmethod
    def make_song_line(position, song_name, length):
        return "`{}. {} | {}`\n\n".format(position, song_name, length)

    @staticmethod
    def make_current_song_line(position, song_name, length):
        return "**{}.** **{} | {}**\n\n".format(position, song_name, length)

    @staticmethod
    def make_arrow_line(point_option):
        if point_option == "previous":
            return "⬆️__Previous__⬆️\n\n"
        elif point_option == "next":
            return "⬇️__Next__⬇️\n\n"
        else:
            return "'{}' isn't a pointing option\n\n".format(point_option)

    @staticmethod
    def make_length_line(playlist):
        total_songs = len(playlist)
        total_length = 0
        for song in playlist:
            total_length += song.get_duration()

        return "\n**{} songs in playlist | {} total length**".format(total_songs, util.format_duration(total_length))

    def get_lines(self):
        next_offset = 0

        # if len(self.playlist_songs) < 11:
        #
        #
        # for i in range

    # def get_line(self, i):
    #     song = None
    #     counter = self.playlist_index + i
    #     adjusted_max = 0
    #     if -4 == i:
    #         adjusted_max = 1
    #     elif -3 == i:
    #         adjusted_max = 2
    #     elif -2 == i:
    #         adjusted_max = 3
    #     elif -1 == i:
    #         adjusted_max = 4
    #
    #     adjusted_index = 0
    #     while True:
    #         if counter < 0 + adjusted_max:
    #             counter += 1
    #         else:
    #             adjusted_index = counter
    #             break
    #
    #     while True:
    #         try:
    #             song = self.playlist_songs[self.playlist_index + adjusted_index]
    #             break
    #         except IndexError:
    #             adjusted_index -= 1
    #
    #     if self.playlist_index + adjusted_index == 0:
    #         return [self.make_arrow_line("next"),
    #                 self.make_current_song_line(self.playlist_index + adjusted_index + 1, song.get_info(
    #                     features.music.song.Song.TITLE), util.format_duration(song.get_duration()))]
    #     elif self.playlist_index + adjusted_index == len(self.playlist_songs) - 1:
    #         return [self.make_current_song_line(self.playlist_index + adjusted_index + 1, song.get_info(
    #             features.music.song.Song.TITLE), util.format_duration(song.get_duration())),
    #                 self.make_arrow_line("previous")]
    #     elif

    # def get_queue_song_lines(self):
    #
    # if self.playlist_index == 0:
    #     for i in range(range_adjustments):
    #         if i == 0:
    #             song_lines += self.make_current_song_line(self.playlist_index + 1, self.current_song.get_info(
    #                 features.music.song.Song.TITLE), util.format_duration(self.current_song.get_duration()))
    #             song_lines += self.make_arrow_line("next")
    #         else:
    #             song = self.playlist_songs[self.playlist_index + i]
    #             song_lines += self.make_song_line(self.playlist_index + i + 1, song.get_info(
    #                 features.music.song.Song.TITLE), util.format_duration(song.get_duration()))
    #
    # elif self.playlist_index == len(self.playlist_songs) - 1:
    #     for i in range(range_adjustments):
    #         if i == range_adjustments - 1:
    #             song_lines += self.make_arrow_line("previous")
    #             song_lines += self.make_current_song_line(self.playlist_index + 1, self.current_song.get_info(
    #                 features.music.song.Song.TITLE), util.format_duration(self.current_song.get_duration()))
    #         else:
    #             song = self.playlist_songs[self.playlist_index - range_adjustments + i + 1]
    #             song_lines += self.make_song_line(self.playlist_index - range_adjustments + i + 2, song.get_info(
    #                 features.music.song.Song.TITLE), util.format_duration(song.get_duration()))

    # def get_queue_embed(self):
    #     song_lines = []
    #
    #     for i in range(-5, 6):
    #         line = self.get_line(i)
    #         if
    #
    #     song_lines.append(self.make_length_line(self.playlist_songs))
    #
    #     text = ""
    #     for line in song_lines:
    #         text += line
    #
    #     return util.make_embed(util.colour_musical, text,
    #                            "Playlist '{}'".format(self.playlist_name), util.image_music_note, None)

    def get_now_playing_embed(self):
        title = "N/A"
        artist = "N/A"
        duration = "N/A"
        length_line = ""

        if self.current_song is not None:
            title = self.current_song.get_info(features.music.song.Song.TITLE)
            artist = self.current_song.get_info(features.music.song.Song.ARTIST)
            duration = util.format_duration(self.current_song.get_duration())

        if self.playlist_songs is not None:
            length_line = self.make_length_line(self.playlist_songs)

        return util.make_embed(colour=util.colour_musical, author_name="Now Playing",
                               author_icon_url=util.image_music_note,
                               description="Title: {}\nArtist: {}\nDuration: {}{}".format(title, artist, duration,
                                                                                          length_line))

    def set_playlist(self, simple_folder):
        self.playlist_songs = []
        if not os.path.isdir(os.path.join(simple_folder)):
            return

        for file in os.listdir(simple_folder):
            if util.is_music_file(os.path.join(simple_folder, file)):
                song = features.music.song.Song(os.path.join(simple_folder, file))
                self.playlist_songs.append(song)
        random.shuffle(self.playlist_songs)
