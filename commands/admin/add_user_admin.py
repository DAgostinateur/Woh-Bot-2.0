import discord
import re

import command_template


class AddUserAdmin(command_template.Command):
    def __init__(self, client):
        super(AddUserAdmin, self).__init__(client)

        self.enabled = True
        self.perm_level = self.permission_owner
        self.cmd_name = "adduseradmin"
        self.arguments = "[user]"
        self.help_description = "Adds the user as an admin for this bot. " \
                                "Grants the user permission to use admin level commands."

    async def command(self, message: discord.Message):
        if not self.execute_cmd(message):
            return

        user_id = self.rm_cmd(message)
        if len(user_id) != 0:
            user_id = re.sub("\D+", "", self.rm_cmd(message))
            if message.server.get_member(user_id) is None:
                await self.send_message_check(message.channel, "Invalid user.")
            else:
                if self.parent_client.admin_handler.get_user_admin(user_id, message.server.id) is not None:
                    await self.send_message_check(message.channel, "User already in the admin list.")
                    return

                self.parent_client.admin_handler.save_user_admin(user_id, message.server.id)
                user = message.server.get_member(user_id)

                await self.send_message_check(message.channel,
                                              "Granted admin commands to {}!".format(user.mention))
        else:
            await self.send_message_check(message.channel, "Invalid user.")
