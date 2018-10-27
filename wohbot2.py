import discord
from datetime import datetime

from features.birthday import birthday_handler
import settings
import hidden
import util


class WohBot(discord.Client):
    data_folder = "data/"

    def __init__(self):
        super(WohBot, self).__init__()

        util.check_folder(self.data_folder)

        self.owner = None
        self.settings = settings.Settings()
        self.birthday_handler = birthday_handler.BirthdayHandler(self)
        self.prefix = "!!!"

        self.loop.create_task(self.birthday_handler.happy_birthday_checker())

    async def _get_client_owner(self):
        app_info = await self.application_info()
        self.owner = app_info.owner

    async def on_ready(self):
        await client.change_presence(game=discord.Game(name="Prefix: !!!", type=0))
        await self._get_client_owner()

        print("-------")
        print("Woh Bot 2.0")
        print("-------")
        print("Logged in as {}".format(self.user))
        print("Creator: {}\n".format(self.owner.name))

    async def on_message(self, message: discord.Message):
        if message.author == self.user:
            return

        if message.content.startswith(self.prefix + "showowner"):
            await self.send_message(message.channel, self.owner.name)

        if 'woh' in message.content.lower():
            if util.get_custom_emoji(list(self.get_all_emojis()), 'woh') is not None:
                await self.add_reaction(message, util.get_custom_emoji(list(self.get_all_emojis()), 'woh'))

    async def on_voice_state_update(self, before: discord.Member, after: discord.Member):
        if before.voice.voice_channel is None and after.voice.voice_channel is not None:
            try:
                print("User Joined VC at {}: {}".format(str(datetime.now().time())[:8], after.name))
            except UnicodeEncodeError:
                print("User Joined VC at {}: {}".format(str(datetime.now().time())[:8], after.id))

        if before.voice.voice_channel is not None and after.voice.voice_channel is None:
            try:
                print("User Left VC at {}: {}".format(str(datetime.now().time())[:8], after.name))
            except UnicodeEncodeError:
                print("User Left VC at {}: {}".format(str(datetime.now().time())[:8], after.id))

    async def on_reaction_add(self, reaction, user):
        if user == self.user:
            return

        # if reaction.emoji == util.get_custom_emoji(list(self.get_all_emojis()), 'woh'):
        if reaction.emoji.name == 'woh':
            await self.add_reaction(reaction.message, reaction.emoji)


if __name__ == '__main__':
    client = WohBot()
    client.run(hidden.token())
