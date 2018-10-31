import discord

from commands import set_presence


class CommandHandler(object):
    def __init__(self, client):
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
        return [set_presence.SetPresence(self.parent_client)]

    async def check_message(self, message: discord.Message):
        for cmd in self.commands:
            await cmd.command(message)

    def get_embed_inlines(self):
        return [cmd.get_help_inline() for cmd in self.commands]

    def enable_command(self, command_name):
        try:
            cmd = self.get_cmd(command_name)
            cmd.enabled = True
        except AttributeError:
            print("FAILED to enable command, '{}' doesn't exist.".format(command_name))

    def disable_command(self, command_name):
        try:
            cmd = self.get_cmd(command_name)
            cmd.enabled = False
        except AttributeError:
            print("FAILED to enable command, '{}' doesn't exist.".format(command_name))
