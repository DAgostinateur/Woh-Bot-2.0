import discord
import random

import hidden
import util


class SpecialReactions:
    woh_emojis = ["woh", "gaywoh1", "gaywoh2", "panwoh1", "panwoh2", "owoh", "wah", "gaoh", "festivewoh",
                  "spookywoh", "transwoh"]
    sans_note_emojis = ["sansD3", "sansD3_2", "sansD4", "sansA3"]

    def __init__(self, client):
        super(SpecialReactions).__init__()
        self.parent_client = client

    @staticmethod
    def get_random_emoji(emoji_list):
        return random.choice(emoji_list)

    async def loop_react(self, message: discord.Message, emoji_list):
        for emoji_name in emoji_list:
            await self.react(message, emoji_name)

    async def react(self, message: discord.Message, emoji_name):
        try:
            await self.parent_client.add_reaction(message, util.get_custom_emoji(self.parent_client, emoji_name))
        except discord.NotFound:
            print("Message probably doesn't exist.")
        except discord.Forbidden:
            print("Client doesn't have permission to send a reaction.")
        except discord.HTTPException:
            print("Emoji '{}' doesn't exist.".format(emoji_name))

    async def check_message(self, message: discord.Message):
        if message.author.id == hidden.pen_id():
            for index, emote in enumerate(self.woh_emojis[1:]):
                if emote in message.content.lower():
                    await self.react(message, emote)
                    break
            else:
                if 'woh' in message.content.lower():
                    await self.react(message, 'woh')
        elif 'woh' in message.content.lower():
            await self.react(message, self.get_random_emoji(self.woh_emojis))

        if 'sans' in message.content.lower():
            await self.loop_react(message, self.sans_note_emojis)

        if 'cringe' in message.content.lower():
            await self.react(message, 'kindacringe')

        if 'epic' in message.content.lower():
            await self.react(message, 'hatdab')
