import discord
import re

import command_template


class Avatar(command_template.Command):
    def __init__(self, client):
        super(Avatar, self).__init__(client)

        self.enabled = True
        self.perm_level = self.permission_levels["everyone"]
        self.cmd_name = "avatar"
        self.arguments = "(user_id)"
        self.help_description = "Shows the avatar of the requested user. Putting nothing shows yours"

    async def get_user(self, message):
        user_id = re.sub("\D+", "", self.rm_cmd(message))
        try:
            user = await self.parent_client.get_user_info(user_id)
        except (discord.NotFound, discord.HTTPException):
            await self.send_message_check(message.channel, "Invalid user id.")
            return None

        return user

    async def command(self, message: discord.Message):
        if not self.execute_cmd(message):
            return

        if len(self.rm_cmd(message)) != 0:
            user = await self.get_user(message)
            if user is None:
                return

            if len(user.avatar_url) == 0:
                await self.send_message_check(message.channel, user.default_avatar_url)
            else:
                await self.send_message_check(message.channel, user.avatar_url)

        else:
            if len(message.author.avatar_url) == 0:
                await self.send_message_check(message.channel, message.author.default_avatar_url)
            else:
                await self.send_message_check(message.channel, message.author.avatar_url)
