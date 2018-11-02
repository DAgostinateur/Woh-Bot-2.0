import discord

import wohbot2
from commands.cant_be_disabled import disable, enable, help
from commands import set_presence


class CommandHandler(object):
    do_not_disable = ["enable", "disable", "help"]

    def __init__(self, client: wohbot2.WohBot):
        self.parent_client = client

        self.commands = self.get_commands()

    def get_cmd(self, command_name):
        """Returns a Command with a command name

        :param command_name:
        :return: Command
        """
        for command in self.commands:
            if command.cmd_name == command_name:
                return command
        return None

    def get_commands(self):
        return [set_presence.SetPresence(self), disable.Disable(self), enable.Enable(self), help.Help(self)]

    async def check_message(self, message: discord.Message):
        for cmd in self.commands:
            await cmd.command(message)

    def get_embed_inlines(self):
        return [cmd.get_help_inline() for cmd in self.commands]

    def enable_command(self, command_name):
        try:
            cmd = self.get_cmd(command_name)
            if cmd in self.do_not_disable:
                return "Attempted to enable an unchangeable command."
            cmd.enabled = True
            return "Enabled '{}'".format(command_name)
        except AttributeError:
            return "Failed to enable command, '{}' doesn't exist.".format(command_name)

    def disable_command(self, command_name):
        try:
            cmd = self.get_cmd(command_name)
            if cmd in self.do_not_disable:
                return "Attempted to disable an unchangeable command."
            cmd.enabled = False
            return "Disabled '{}'".format(command_name)
        except AttributeError:
            return "Failed to disable command, '{}' doesn't exist.".format(command_name)
