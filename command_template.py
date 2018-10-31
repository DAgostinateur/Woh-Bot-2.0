import discord

import wohbot2
import util


class Command(object):
    permission_none = 0  # Command access: Nobody
    permission_everyone = 1  # Command access: Everyone
    permission_admin = 2  # Command access: Admin Users (made admin by me) and me
    permission_owner = 3  # Command access: Me

    colour_royal_purple = 7885225

    def __init__(self, client: wohbot2.WohBot):
        self.parent_client = client

        self.enabled = False
        self.cmd_id = None
        self.perm_level = self.permission_none
        self.cmd_name = ""
        self.arguments = ""
        self.help_description = ""

    def __eq__(self, other):
        return self.cmd_id == other.cmd_id

    def get_help_embedded(self):
        title = "Command Name: {}".format(self.cmd_name)
        description = "\nUse: {}{} {}\n\n{}".format(self.parent_client.prefix, self.cmd_name,
                                                    self.arguments, self.help_description)
        return discord.Embed(title=title, description=description, colour=self.colour_royal_purple)

    def get_help_inline(self):
        return {"name": "{} {}".format(self.cmd_name, self.arguments), "value": self.help_description}

    def get_cmd(self, message: discord.Message):
        return message.content[:len(self.parent_client.prefix + self.cmd_name)]

    def rm_cmd(self, message: discord.Message):
        return message.content[len(self.parent_client.prefix + self.cmd_name):].lstrip()

    def cmd_called(self, message: discord.Message):
        return self.get_cmd(message).lower() == self.parent_client.prefix + self.cmd_name

    def has_permission(self, perms, user_id, server_id):
        if perms == self.permission_none:
            return False
        elif perms == self.permission_everyone:
            return True
        elif perms == self.permission_admin:
            return self.parent_client.admin_handler.is_user_admin(user_id, server_id)
        elif perms == self.permission_owner:
            return util.is_owner(user_id)
        return False

    def execute_cmd(self, message: discord.Message):
        if not self.enabled:
            return False

        if not self.cmd_called(message):
            return False

        if not self.has_permission(self.perm_level, message.author.id, message.server.id):
            return False

        return True
