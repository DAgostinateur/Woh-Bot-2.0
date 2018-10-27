import discord

import util


class Command(object):
    permission_none = 0  # Command access: Nobody
    permission_everyone = 1  # Command access: Everyone
    permission_admin = 2  # Command access: Admin Users (made admin by me) and me
    permission_owner = 3  # Command access: Me

    def __init__(self, client: discord.Client):
        self.parent_client = client

        self.enabled = False
        self.perm_level = self.permission_none
        self.cmd_name = ""
        self.help_description = ""
        self.expanded_help_description = ""

    def get_cmd(self, message: discord.Message):
        return message.content[:len(self.parent_client.prefix + self.cmd_name)]

    def rm_cmd(self, message: discord.Message):
        return message.content[len(self.parent_client.prefix + self.cmd_name):].lstrip()

    def cmd_called(self, message: discord.Message):
        return self.get_cmd(message) == self.parent_client.prefix + self.cmd_name

    def has_permission(self, perms, user_id):
        if perms == self.permission_none:
            return False
        elif perms == self.permission_everyone:
            return True
        elif perms == self.permission_admin:
            return False  # Have to make an admin user class
        elif perms == self.permission_owner:
            return util.is_owner(user_id)
        return False

    async def execute_cmd(self, message: discord.Message):
        if not self.enabled:
            return False

        if not self.cmd_called(message):
            return False

        if not self.has_permission(self.perm_level, message.author.id):
            return False

        return True
