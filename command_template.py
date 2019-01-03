import discord
import re

import util


class Command(object):
    permission_levels = {"none": 0, "everyone": 1, "admin": 2, "owner": 3}

    def __init__(self, handler):
        self.handler = handler

        self.enabled = False
        self.perm_level = self.permission_levels["none"]
        self.cmd_name = ""
        self.arguments = ""
        self.option_letters = ""  # Example: w!listuserbd -da
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
        title = "Command Name: {}".format(self.cmd_name.upper())
        description = "\nState: {}\nPermission Level: {}\n" \
                      "Use: {}{} {}\n\n{}".format(self.get_state_name(), self.get_permission_name(self.perm_level),
                                                  self.parent_client.prefix, self.cmd_name, self.arguments,
                                                  self.help_description)
        return discord.Embed(title=title, description=description, colour=util.colour_royal_purple)

    def get_help_inline(self):
        return {"name": "{} - {} - {}{} {}".format(self.get_state_name(), self.get_permission_name(self.perm_level),
                                                   self.parent_client.prefix, self.cmd_name.upper(), self.arguments),
                "value": self.help_description, "inline": "true"}

    def rm_cmd(self, message: discord.Message):
        return message.content[len(self.parent_client.prefix + self.cmd_name):].lstrip()

    def get_permission_name(self, perms):
        if perms == self.permission_levels["none"]:
            return "No one"
        elif perms == self.permission_levels["everyone"]:
            return "Everyone"
        elif perms == self.permission_levels["admin"]:
            return "Admin"
        elif perms == self.permission_levels["owner"]:
            return "Bot Owner"
        else:
            return "Perms broken"

    def get_state_name(self):
        if self.enabled:
            return "Enabled"
        else:
            return "Disabled"

    def has_permission(self, perms, user_id, server_id):
        if perms == self.permission_levels["none"]:
            return False
        elif perms == self.permission_levels["everyone"]:
            return True
        elif perms == self.permission_levels["admin"]:
            return self.parent_client.admin_handler.is_user_admin(user_id, server_id) or util.is_owner(user_id)
        elif perms == self.permission_levels["owner"]:
            return util.is_owner(user_id)
        return False

    def has_wanted_argument(self, message, wanted_letters: str):
        # wanted_letters can't be empty
        argument = self.check_argument_options(message)
        if argument is None:
            return False

        true_counter = len(wanted_letters)
        for arg_letter in argument[1:]:
            if arg_letter in wanted_letters:
                true_counter -= 1

        return true_counter == 0

    def check_argument_options(self, message: discord.Message):
        if len(self.option_letters) != 0:
            pattern = r"-[" + self.option_letters + r"]{,3}$"
            regex = re.compile(pattern)
            argument = regex.search(self.rm_cmd(message))
            if argument is not None:
                return argument.group()
        return None

    def execute_cmd(self, message: discord.Message):
        if not self.enabled:
            return False

        if not self.has_permission(self.perm_level, message.author.id, message.server.id):
            return False

        return True

    async def send_message_check(self, channel: discord.Channel, text=None, embed=None):
        try:
            await self.parent_client.send_message(channel, content=text, embed=embed)
        except discord.NotFound:
            print("Channel '{}' probably doesn't exist.".format(channel.id))
        except discord.Forbidden:
            print("Client doesn't have permission to send a message in '{}'.".format(channel.id))
