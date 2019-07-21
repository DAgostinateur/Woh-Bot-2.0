import discord

import command_template


class Search(command_template.Command):
    def __init__(self, client):
        super(Search, self).__init__(client)

        self.enabled = True
        self.perm_level = self.permission_levels["everyone"]
        self.cmd_name = "search"
        self.arguments = "[song]"
        self.help_description = "Searches the currently playing playlist for a song."

    async def command(self, message: discord.Message):
        if not self.execute_cmd(message):
            return

        search_input = self.rm_cmd(message)

        if self.parent_client.music_handler.is_in_vc(message):
            if self.parent_client.music_handler.playlist_songs is None:
                await self.send_message_check(message.channel, "There's no playlist on.")
                return

            if len(search_input) != 0:
                text_output = await self.parent_client.music_handler.search(search_input)
                await self.send_message_check(message.channel, text_output)
            else:
                await self.send_message_check(message.channel, "Can't search with nothing.")
        else:
            await self.send_message_check(message.channel, "There's nothing playing.")
