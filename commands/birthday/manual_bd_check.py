import discord

import command_template


class ManualBDCheck(command_template.Command):
    def __init__(self, client):
        super(ManualBDCheck, self).__init__(client)

        self.enabled = True
        self.perm_level = self.permission_levels["owner"]
        self.cmd_name = "manualbd"
        self.arguments = ""
        self.help_description = "Check if it's anyone's birthday manually."

    async def command(self, message: discord.Message):
        if not self.execute_cmd(message):
            return

        await self.parent_client.birthday_handler.happy_birthday_checker()
        await self.send_message_check(message.channel, "Check done.")
