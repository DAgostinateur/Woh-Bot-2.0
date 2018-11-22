import aiohttp
import discord
from datetime import datetime

from features.admin import admin_handler
from features.birthday import birthday_handler
from features import special_reactions, command_handler, ping_for_help

import settings
import hidden
import util


# TODO:
# Remake the help command, there's too many commands displayed, drowns the channel.
# Better way to load commands.
# Set different prefixes for servers.
# Proper Logging.
# Music. Only to support my local playlist.
# Control Terraria Server, basically finish what I started with the first bot.


class WohBot(discord.Client):
    data_folder = "data/"

    def __init__(self):
        super(WohBot, self).__init__()

        util.check_folder(self.data_folder)

        self.prefix = "w!"
        self.default_presence = "Prefix: " + self.prefix
        self.owner = None
        self.settings = settings.Settings()

        self.admin_handler = admin_handler.AdminHandler(self)
        self.birthday_handler = birthday_handler.BirthdayHandler(self)
        self.special_reactions = special_reactions.SpecialReactions(self)
        self.command_handler = command_handler.CommandHandler(self)
        self.ping_for_help = ping_for_help.PingForHelp(self)  # This needs a better name

        self.loop.create_task(self.birthday_handler.happy_birthday_checker())

    async def _get_client_owner(self):
        app_info = await self.application_info()
        self.owner = app_info.owner

    async def on_ready(self):
        self.birthday_handler.check_birthday_lists()

        await client.change_presence(game=discord.Game(name=self.default_presence, type=0))
        await self._get_client_owner()

        print("-------")
        print("Woh Bot 2.0")
        print("-------")
        print("Logged in as {}".format(self.user))
        print("Creator: {}".format(self.owner.name))
        print("Prefix: {}".format(self.prefix))
        print("-------\n")

    async def on_message(self, message: discord.Message):
        if message.author == self.user:
            return

        if not message.channel.is_private:
            await self.special_reactions.check_message(message)
            await self.command_handler.check_message(message)
            await self.ping_for_help.check_message(message)

    async def on_member_join(self, member: discord.Member):
        try:
            print("User Joined Server '{}' at {} - {}".format(member.server.name, str(datetime.now().time())[:8],
                                                              member.name))
        except UnicodeEncodeError:
            print("User Joined Server '{}' at {} - {}".format(member.server.id, str(datetime.now().time())[:8],
                                                              member.id))

    async def on_member_remove(self, member: discord.Member):
        try:
            print("User Left Server '{}' at {} - {}".format(member.server.name, str(datetime.now().time())[:8],
                                                            member.name))
        except UnicodeEncodeError:
            print(
                "User Left Server '{}' at {} - {}".format(member.server.id, str(datetime.now().time())[:8], member.id))

    async def on_voice_state_update(self, before: discord.Member, after: discord.Member):
        if before.voice.voice_channel is None and after.voice.voice_channel is not None:
            try:
                print("User Joined VC in '{}' at {} - {}".format(after.server.name, str(datetime.now().time())[:8],
                                                                 after.name))
            except UnicodeEncodeError:
                print("User Joined VC in '{}' at {} - {}".format(after.server.id, str(datetime.now().time())[:8],
                                                                 after.id))

        if before.voice.voice_channel is not None and after.voice.voice_channel is None:
            try:
                print("User Left VC in '{}' at {} - {}".format(after.server.name, str(datetime.now().time())[:8],
                                                               after.name))
            except UnicodeEncodeError:
                print("User Left VC in '{}' at {} - {}".format(after.server.id, str(datetime.now().time())[:8],
                                                               after.id))

    async def on_reaction_add(self, reaction, user):
        if user == self.user:
            return

        if type(reaction.emoji) is discord.Emoji:
            if reaction.emoji.name == 'woh':
                await self.add_reaction(reaction.message, reaction.emoji)


if __name__ == '__main__':
    try:
        print(str(datetime.today()))
        client = WohBot()
        client.run(hidden.token())
    except ConnectionResetError:
        print("No Internet connection.")
        exit(1)
    except aiohttp.ClientOSError:
        print("Could not connect to Discord.")
        exit(1)
