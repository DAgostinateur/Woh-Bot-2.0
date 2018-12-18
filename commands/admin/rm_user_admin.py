import discord
import re

import command_template


class RmUserAdmin(command_template.Command):
    def __init__(self, client):
        super(RmUserAdmin, self).__init__(client)

        self.enabled = True
        self.perm_level = self.permission_levels["owner"]
        self.cmd_name = "rmuseradmin"
        self.arguments = "[user]"
        self.help_description = "Removes the user as an admin for this bot. " \
                                "Strips the user's permission to use admin level commands."

    async def command(self, message: discord.Message):
        if not self.execute_cmd(message):
            return

        user_id = self.rm_cmd(message)
        if len(user_id) != 0:
            user_id = re.sub("\D+", "", self.rm_cmd(message))
            if message.server.get_member(user_id) is None:
                await self.send_message_check(message.channel, "Invalid user.")
            else:
                if self.parent_client.admin_handler.get_user_admin(user_id, message.server.id) is None:
                    await self.send_message_check(message.channel, "User is not in the admin list.")
                    return

                self.parent_client.admin_handler.remove_user_admin(user_id, message.server.id)
                user = message.server.get_member(user_id)

                await self.send_message_check(message.channel,
                                              "Removed admin commands from {}!".format(user.mention))
        else:
            await self.send_message_check(message.channel, "Invalid user.")
