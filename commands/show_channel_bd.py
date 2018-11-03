import discord

import util
import command_template


class ShowChannelBD(command_template.Command):
    def __init__(self, client):
        super(ShowChannelBD, self).__init__(client)

        self.enabled = True
        self.perm_level = self.permission_admin
        self.cmd_name = "showchannelbd"
        self.arguments = ""
        self.help_description = "Shows the channel used for birthday messages."

    async def command(self, message: discord.Message):
        if not self.execute_cmd(message):
            return

        channel_bd = self.parent_client.birthday_handler.get_channel_bd(message.server.id)
        if channel_bd is None:
            try:
                await self.parent_client.send_message(message.channel, "No Birthday Channel was set on this server.")
            except discord.Forbidden:
                print("Client doesn't have permission to send a message in '{}'.".format(message.channel.id))
        else:
            try:
                await self.parent_client.send_message(message.channel,
                                                      "The Birthday Channel for this server is {}.".format(
                                                          util.channel_format(channel_bd.channel_id)))
            except discord.Forbidden:
                print("Client doesn't have permission to send a message in '{}'.".format(message.channel.id))
