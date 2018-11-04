import discord
import datetime

import command_template


class SetUserBD(command_template.Command):
    def __init__(self, client):
        super(SetUserBD, self).__init__(client)

        self.enabled = True
        self.perm_level = self.permission_everyone
        self.cmd_name = "setuserbd"
        self.arguments = "(MM-DD)"
        self.help_description = "Sets the birthday of the user. It will ping them on their birthday this server. " \
                                "Putting nothing in (MM-DD) removes it."

    @staticmethod
    def validate_date(date_text):
        try:
            str(datetime.datetime.strptime(date_text, '%m-%d'))
            return True
        except ValueError:
            return False

    async def command(self, message: discord.Message):
        if not self.execute_cmd(message):
            return

        mm_dd = self.rm_cmd(message)
        if len(mm_dd) != 0:
            if not self.validate_date(mm_dd):
                try:
                    await self.parent_client.send_message(message.channel, "Invalid date.")
                except discord.Forbidden:
                    print("Client doesn't have permission to send a message in '{}'.".format(message.channel.id))
            else:
                self.parent_client.birthday_handler.save_user_birthday(message.author.id, mm_dd, message.server.id)
                user_bd = self.parent_client.birthday_handler.get_user_bd(message.author.id, message.server.id)
                try:
                    await self.parent_client.send_message(message.channel,
                                                          "Your birthday has been set for {} {}.".format(
                                                              user_bd.get_readable_month(), user_bd.get_readable_day()))
                except discord.Forbidden:
                    print("Client doesn't have permission to send a message in '{}'.".format(message.channel.id))
        else:
            self.parent_client.birthday_handler.remove_user_birthday(message.author.id, message.server.id)
            await self.send_message_check_forbidden(message, "Your birthday was removed.")
