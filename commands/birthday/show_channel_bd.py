import discord

import util
import command_template


class ShowChannelBD(command_template.Command):
    def __init__(self, client):
        super(ShowChannelBD, self).__init__(client)

        self.enabled = True
        self.perm_level = self.permission_levels["admin"]
        self.cmd_name = "showchannelbd"
        self.help_description = "Shows the channel used for birthday messages."

    async def command(self, message: discord.Message):
        if not self.execute_cmd(message):
            return

        channel_bd = self.parent_client.birthday_handler.get_channel_bd(message.server.id)
        if channel_bd is None:
            await self.send_message_check(message.channel, "No birthday channel is set on this server.")
        else:
            await self.send_message_check(message.channel, "The birthday channel for this server is {}!".format(
                util.channel_format(channel_bd.channel_id)))
