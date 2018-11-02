import discord

import util


class Command(object):
    permission_none = 0  # Command access: Nobody
    permission_everyone = 1  # Command access: Everyone
    permission_admin = 2  # Command access: Admin Users (made admin by me) and me
    permission_owner = 3  # Command access: Me

    colour_royal_purple = 7885225

    def __init__(self, handler):
        self.handler = handler

        self.enabled = False
        self.perm_level = self.permission_none
        self.cmd_name = ""
        self.arguments = ""
        self.help_description = ""

    def __eq__(self, other):
        if type(other) is str:
            return self.cmd_name == other
        else:
            return self.cmd_name == other.cmd_name

    @property
    def parent_client(self):
        return self.handler.parent_client

    def get_help_embedded(self):
        title = "Command Name: {}".format(self.cmd_name)
        description = "\nPermission Level: {}\nUse: {}{} {}\n\n{}".format(self.get_permission_name(self.perm_level),
                                                                          self.parent_client.prefix, self.cmd_name,
                                                                          self.arguments, self.help_description)
        return discord.Embed(title=title, description=description, colour=self.colour_royal_purple)

    def get_help_inline(self):

        return {"name": "{} - {}{} {}".format(self.get_permission_name(self.perm_level), self.parent_client.prefix,
                                              self.cmd_name, self.arguments),
                "value": self.help_description}

    def get_cmd(self, message: discord.Message):
        return message.content[:len(self.parent_client.prefix + self.cmd_name)]

    def rm_cmd(self, message: discord.Message):
        return message.content[len(self.parent_client.prefix + self.cmd_name):].lstrip()

    def cmd_called(self, message: discord.Message):
        return self.get_cmd(message).lower() == self.parent_client.prefix + self.cmd_name

    def get_permission_name(self, perms):
        if perms == self.permission_none:
            return "No one"
        elif perms == self.permission_everyone:
            return "Everyone"
        elif perms == self.permission_admin:
            return "Admin"
        elif perms == self.permission_owner:
            return "Owner"
        else:
            return "Perms broken"

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