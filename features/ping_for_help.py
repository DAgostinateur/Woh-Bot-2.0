import discord
import re


class PingForHelp:
    def __init__(self, client):
        super(PingForHelp).__init__()
        self.parent_client = client

    def pinged_client(self, message: discord.Message):
        # Only a ping
        regex = re.compile(r"(^<@\d+>$|^<@!\d+>$)")
        argument = regex.search(message.content)
        if argument is None:
            return False

        # Client ping
        user_id = re.sub("\D+", "", argument.group())
        if message.server.get_member(user_id) is None:
            return False
        else:
            return user_id == self.parent_client.user.id

    async def check_message(self, message: discord.Message):
        if self.pinged_client(message):
            try:
                await self.parent_client.send_message(message.channel,
                                                      "Prefix for this server: {0}\nHelp Command: {0}help".format(
                                                          self.parent_client.prefix))
            except discord.Forbidden:
                print("Client doesn't have permission to send a message in '{}'.".format(message.channel.id))
