import discord
import re

import util
import command_template


class SetChannelBD(command_template.Command):
    def __init__(self, client):
        super(SetChannelBD, self).__init__(client)

        self.enabled = True
        self.perm_level = self.permission_admin
        self.cmd_name = "setchannelbd"
        self.arguments = "(channel)"
        self.help_description = "Sets the channel used for birthday messages. Putting nothing in (channel) removes it."

    async def command(self, message: discord.Message):
        if not self.execute_cmd(message):
            return

        channel_id = self.rm_cmd(message)
        if len(channel_id) != 0:
            channel_id = re.sub("\D+", "", self.rm_cmd(message))
            if message.server.get_channel(channel_id) is None:
                await self.send_message_check(message.channel, "Invalid channel.")
            else:
                self.parent_client.birthday_handler.save_channel_birthday(channel_id, message.server.id)
                await self.send_message_check(message.channel, "Birthday channel changed to {}!".format(
                    util.channel_format(channel_id)))
        else:
            self.parent_client.birthday_handler.remove_channel_birthday(message.server.id)
            await self.send_message_check(message.channel, "Birthday channel removed!")
