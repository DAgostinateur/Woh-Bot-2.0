import discord

import command_template


class Disable(command_template.Command):
    def __init__(self, handler):
        super(Disable, self).__init__(handler)

        self.enabled = True  # Should never change
        self.perm_level = self.permission_owner
        self.cmd_name = "disable"
        self.arguments = "[command]"
        self.help_description = "Disables a command from the bot. This command can not be disabled."

    async def command(self, message: discord.Message):
        if not self.execute_cmd(message):
            return

        text_result = self.handler.disable_command(self.rm_cmd(message))
        try:
            await self.parent_client.send_message(message.channel, text_result)
        except discord.Forbidden:
            print("Client doesn't have permission to send a message in '{}'.".format(message.channel.id))
