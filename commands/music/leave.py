import discord

import command_template


class Leave(command_template.Command):
    def __init__(self, client):
        super(Leave, self).__init__(client)

        self.enabled = True
        self.perm_level = self.permission_levels["everyone"]
        self.cmd_name = "leave"
        self.arguments = ""
        self.help_description = "Leaves the voice chat."

    async def command(self, message: discord.Message):
        if not self.execute_cmd(message):
            return

        if len(self.parent_client.voice_clients) != 0:
            vc = self.parent_client.voice_client_in(message.server)
            if vc is not None:
                if message.author.voice.voice_channel is not None:
                    self.parent_client.music_handler.reset()
                    await vc.disconnect()
