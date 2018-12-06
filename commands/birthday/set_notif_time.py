import discord

import command_template
import util


class SetNotifTime(command_template.Command):
    def __init__(self, client):
        super(SetNotifTime, self).__init__(client)

        self.enabled = True
        self.perm_level = self.permission_owner
        self.cmd_name = "setnotiftime"
        self.arguments = "(hour)"
        self.help_description = "Sets the time when the bot will send birthday messages. (hour) is the hour in the " \
                                "day in EST. Putting nothing in (hour) resets it."

    async def command(self, message: discord.Message):
        if not self.execute_cmd(message):
            return

        hour = self.rm_cmd(message)
        if len(hour) != 0:
            if not util.is_int(hour):
                await self.send_message_check(message.channel, "Invalid hour.")
                return

            hour = int(hour)
            if not (0 <= hour <= 23):
                await self.send_message_check(message.channel, "Invalid hour.")
            else:
                self.parent_client.settings.save_user_defaults(notification_time=hour)
                await self.send_message_check(message.channel,
                                              "Birthday messages will be sent at {}:00 EST!".format(hour))
        else:
            self.parent_client.settings.save_user_defaults(
                notification_time=self.parent_client.settings.default_bot_notification_time)
            await self.send_message_check(message.channel, "Notification time back to default!")
