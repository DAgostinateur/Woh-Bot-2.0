import discord

import command_template


class ShowMessageBD(command_template.Command):
    def __init__(self, client):
        super(ShowMessageBD, self).__init__(client)

        self.enabled = True
        self.perm_level = self.permission_levels["admin"]
        self.cmd_name = "showmessagebd"
        self.help_description = "Shows the message used for birthday messages."

    async def command(self, message: discord.Message):
        if not self.execute_cmd(message):
            return

        message_bd = self.parent_client.birthday_handler.get_message_bd(message.server.id)
        if message_bd is None:
            await self.send_message_check(message.channel, "No birthday message is set on this server!")
        else:
            await self.send_message_check(message.channel, "The birthday message for this server is '{}'!".format(
                message_bd.birthday_message))
