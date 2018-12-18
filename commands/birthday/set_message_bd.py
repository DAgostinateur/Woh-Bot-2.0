import discord

import command_template


class SetMessageBD(command_template.Command):
    def __init__(self, client):
        super(SetMessageBD, self).__init__(client)

        self.enabled = True
        self.perm_level = self.permission_levels["admin"]
        self.cmd_name = "setmessagebd"
        self.arguments = "(message)"
        self.help_description = "Sets the message used for birthday messages. Putting nothing in (message) removes it."

    async def command(self, message: discord.Message):
        if not self.execute_cmd(message):
            return

        text = self.rm_cmd(message)
        if len(text) != 0:
            if self.parent_client.birthday_handler.get_message_bd(message.server.id) is not None:
                self.parent_client.birthday_handler.remove_message_birthday(message.server.id)

            self.parent_client.birthday_handler.save_message_birthday(message.server.id, text)
            await self.send_message_check(message.channel, "Birthday message changed to '{}'!".format(text))
        else:
            self.parent_client.birthday_handler.remove_message_birthday(message.server.id)
            await self.send_message_check(message.channel, "Birthday message removed!")
