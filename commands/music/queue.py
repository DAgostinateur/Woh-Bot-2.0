import discord

import command_template


class Queue(command_template.Command):
    def __init__(self, client):
        super(Queue, self).__init__(client)

        self.enabled = True
        self.perm_level = self.permission_levels["everyone"]
        self.cmd_name = "q"
        self.arguments = ""
        self.help_description = "Displays the current and 10 closest songs in the queue."

    async def command(self, message: discord.Message):
        if not self.execute_cmd(message):
            return

        if self.parent_client.music_handler.is_in_vc(message):
            if self.parent_client.music_handler.playlist_songs is not None:
                pass
                embed = self.parent_client.music_handler.get_queue_embed()
                await  self.send_message_check(message.channel, embed=embed)
            else:
                await self.send_message_check(message.channel, "There's no playlist on, use 'np' instead.")
        else:
            await self.send_message_check(message.channel, "There's nothing playing.")
