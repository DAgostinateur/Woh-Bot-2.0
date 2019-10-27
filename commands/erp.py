import discord

import command_template


# Requested by Waffle.
class Erp(command_template.Command):
    def __init__(self, client):
        super(Erp, self).__init__(client)

        self.enabled = True
        self.perm_level = self.permission_levels["everyone"]
        self.cmd_name = "erp"
        self.arguments = ""
        self.help_description = "please take your erp to dms"

    async def command(self, message: discord.Message):
        if not self.execute_cmd(message):
            return

        await self.send_message_check(message.channel, "https://cdn.discordapp.com/attachments/"
                                                       "458058017641070602/617418069408612420/unknown.png")
