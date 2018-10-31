import discord

import command_template


class SetPresence(command_template.Command):
    def __init__(self, client):
        super(SetPresence, self).__init__(client)

        self.enabled = True
        self.cmd_id = 1001
        self.perm_level = self.permission_owner
        self.cmd_name = "setpresence"
        self.arguments = "(game)"
        self.help_description = "Sets the bot's presence. Putting nothing in (game) resets the presence."

    async def change_presence(self, message, game_name, text):
        game = discord.Game(name=game_name, type=0)
        await self.parent_client.change_presence(game=game)
        try:
            await self.parent_client.send_message(message.channel, text)
        except discord.Forbidden:
            print("Client doesn't have permission to send a message in '{}'.".format(message.channel.id))

    async def command(self, message: discord.Message):
        if not self.execute_cmd(message):
            return

        game_name = self.rm_cmd(message)
        if len(game_name) != 0:
            await self.change_presence(message, game_name, "Changed presence!")

        else:
            await self.change_presence(message, self.parent_client.default_presence, "Presence back to default!")
