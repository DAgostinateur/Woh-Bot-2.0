import discord

import command_template
import util


class Volume(command_template.Command):
    def __init__(self, client):
        super(Volume, self).__init__(client)

        self.enabled = True
        self.perm_level = self.permission_everyone
        self.cmd_name = "volume"
        self.arguments = "(number)"
        self.help_description = "Sets the volume for the bot. Between 0 and 100, nothing puts it back to default."

    async def command(self, message: discord.Message):
        if not self.execute_cmd(message):
            return

        number = self.rm_cmd(message)

        if len(number) == 0:
            output_text = "Volume back to default. " + self.parent_client.music_handler.set_volume(
                self.parent_client.music_handler.default_volume)
            await self.send_message_check(message.channel, output_text)
            return

        if util.is_int(number):
            if 0 <= int(number) <= 100:
                vol = int(number) / 100
                output_text = self.parent_client.music_handler.set_volume(vol)
                await self.send_message_check(message.channel, output_text)
            else:
                await self.send_message_check(message.channel, "Number has to be between 0 and 100.")
        else:
            await self.send_message_check(message.channel, "Has to be a number.")
