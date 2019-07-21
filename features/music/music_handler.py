import discord
import os
import asyncio
import random
import difflib

import util
import features.music.song


class MusicHandler(object):
    music_folder = "data/music"
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
                    await asyncio.sleep(4)
                    await self.send_message_check(self.activated_in_channel, "Playlist ended.")
                    await self.leave_vc()
            else:
                await self.send_message_check(self.activated_in_channel,
                                              "Nobody has been in this voice channel for 10 minutes, bi bye.")
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
                                          "'hqplaylist' plays D'Agostinatrice Woh's entire playlist.")
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

    async def next(self, skip=1):
        self.player.stop()

        if self.playlist_index >= len(self.playlist_songs) - 1:
            await self.send_message_check(self.activated_in_channel, "Playlist ended.")
            await self.leave_vc()
            return

        self.playlist_index += skip

        if self.playlist_index >= len(self.playlist_songs) - 1:
            self.playlist_index = len(self.playlist_songs) - 1

        await self.make_player(self.playlist_songs[self.playlist_index])

    async def previous(self, back=1):
        self.player.stop()
        self.playlist_index -= back
        if 0 > self.playlist_index:
            self.playlist_index = 0

        await self.make_player(self.playlist_songs[self.playlist_index])

    async def search(self, searched_song):
        title_list = []
        for song in self.playlist_songs:
            title_list.append(song.get_info(features.music.song.Song.TITLE))

        song_title_found = difflib.get_close_matches(searched_song, title_list, n=1, cutoff=0.5)
        if len(song_title_found) == 0:
            return "No song found using '{}'".format(searched_song)

        for index, song in enumerate(self.playlist_songs):
            if song_title_found[0] == song.get_info(features.music.song.Song.TITLE):
                self.player.stop()
                util.swap_position(self.playlist_songs, self.playlist_index, index)
                await self.make_player(self.playlist_songs[self.playlist_index])
                return "Song '{}' found.".format(song_title_found)

        return "Something broke '{}'".format(song_title_found)

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
        return "`{}. {} | {}`\n\n".format(position, song_name, util.format_duration(length))

    @staticmethod
    def make_current_song_line(position, song_name, length):
        return "**{}.** **{} | {}**\n\n".format(position, song_name, util.format_duration(length))

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

    def get_queue_embed(self):
        song_lines = []

        starting_range = 0
        ending_range = 11

        if len(self.playlist_songs) < 11:
            ending_range = len(self.playlist_songs)
        else:
            if 5 < self.playlist_index < len(self.playlist_songs) - 6:
                starting_range = self.playlist_index - 5
                ending_range = self.playlist_index + 6
            elif self.playlist_index > len(self.playlist_songs) - 7:
                starting_range = len(self.playlist_songs) - 11
                ending_range = len(self.playlist_songs)

        for i in range(starting_range, ending_range):
            song = self.playlist_songs[i]
            if i == self.playlist_index:
                if 0 == self.playlist_index:
                    song_lines.append(self.make_current_song_line(i + 1, song.get_info(features.music.song.Song.TITLE),
                                                                  song.get_duration()))
                    song_lines.append(self.make_arrow_line("next"))
                elif len(self.playlist_songs) - 1 == self.playlist_index:
                    song_lines.append(self.make_arrow_line("previous"))
                    song_lines.append(self.make_current_song_line(i + 1, song.get_info(features.music.song.Song.TITLE),
                                                                  song.get_duration()))
                else:
                    song_lines.append(self.make_arrow_line("previous"))
                    song_lines.append(self.make_current_song_line(i + 1, song.get_info(features.music.song.Song.TITLE),
                                                                  song.get_duration()))
                    song_lines.append(self.make_arrow_line("next"))
            else:
                song_lines.append(
                    self.make_song_line(i + 1, song.get_info(features.music.song.Song.TITLE), song.get_duration()))

        song_lines.append(self.make_length_line(self.playlist_songs))

        text = ""
        for line in song_lines:
            text += line

        return util.make_embed(colour=util.colour_musical, description=text, author_icon_url=util.image_music_note,
                               author_name="Playlist '{}'".format(self.playlist_name))

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
