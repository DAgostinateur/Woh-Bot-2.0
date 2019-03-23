import aiohttp
import discord
import time
from datetime import datetime

from features.admin import admin_handler
from features.birthday import birthday_handler
from features.bot_logging import logging_handler
from features.music import music_handler
from features import special_reactions, command_handler, ping_for_help

import settings
import hidden
import util


# TODO:
# Aliases for commands.
# Flatter code.
# Remake the help command, there's too many commands displayed, drowns the channel.
# Better way to load commands.
# Set different prefixes for servers.
# Proper Logging.
# Control any self hosted servers, basically finish what I started with the first bot.


class WohBot(discord.Client):
    data_folder = "data/"

    def __init__(self):
        super(WohBot, self).__init__()

        self.version = "2.1.01"

        util.check_folder(self.data_folder)

        self.prefix = "w!"
        self.default_presence = "Prefix: " + self.prefix
        self.owner = None
        self.settings = settings.Settings()

        self.admin_handler = admin_handler.AdminHandler(self)
        self.birthday_handler = birthday_handler.BirthdayHandler(self)
        self.logging_handler = logging_handler.LoggingHandler(self)
        self.music_handler = music_handler.MusicHandler(self)
        self.special_reactions = special_reactions.SpecialReactions(self)
        self.command_handler = command_handler.CommandHandler(self)
        self.ping_for_help = ping_for_help.PingForHelp(self)  # This needs a better name

        self.loop.create_task(self.birthday_handler.birthday_timer())
        self.loop.create_task(self.music_handler.disconnect_timer())

    async def _get_client_owner(self):
        app_info = await self.application_info()
        self.owner = app_info.owner

    async def on_ready(self):
        # self.birthday_handler.check_birthday_lists()

        await client.change_presence(game=discord.Game(name=self.default_presence, type=0))
        await self._get_client_owner()
        self.logging_handler.temporary_channel = self.get_channel("533832271057125397")

        print("-------")
        print("Woh Bot 2.0")
        print("-------")
        print("Logged in as " + str(self.user))
        print("Creator: " + self.owner.name)
        print("Prefix: " + self.prefix)
        print("Version: " + self.version)
        print("-------\n")

    async def on_message(self, message: discord.Message):
        if message.author == self.user:
            return

        if not message.channel.is_private:
            await self.special_reactions.check_message(message)
            await self.command_handler.check_message(message)
            await self.ping_for_help.check_message(message)

    async def on_member_join(self, member: discord.Member):
        await self.logging_handler.on_member_join(member)

    async def on_member_remove(self, member: discord.Member):
        await self.logging_handler.on_member_remove(member)

    async def on_voice_state_update(self, before: discord.Member, after: discord.Member):
        await self.logging_handler.on_voice_state_update(before, after)

    async def on_reaction_add(self, reaction, user):
        if user == self.user:
            return

        if type(reaction.emoji) is discord.Emoji:
            if reaction.emoji.name == 'woh':
                await self.add_reaction(reaction.message, reaction.emoji)


if __name__ == '__main__':
    print(str(datetime.today()))
    try:
        client = WohBot()
        client.run(hidden.token())
    except RuntimeError:
        print("A task broke.")
    except ConnectionResetError:
        print("No Internet connection.")
    except aiohttp.ClientOSError:
        print("Could not connect to Discord.")
    time.sleep(4)
