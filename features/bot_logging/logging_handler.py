import discord
import pytz

from datetime import datetime, timedelta

import util
import wohbot2


class LoggingHandler(object):
    log_types = {"voice_join": 0, "voice_leave": 1, "member_join": 2, "member_leave": 3}

    def __init__(self, client: wohbot2.WohBot):
        self.parent_client = client

        self.temporary_channel = None

    @staticmethod
    def print_member_updates(text: str, member: discord.Member):
        member_name = member.name
        server_name = member.server.name
        if not util.is_printable(member_name):
            member_name = member.id

        if not util.is_printable(server_name):
            server_name = member.server.id

        print(text.format(server_name, str(datetime.now().time())[:8], member_name))

    async def on_member_join(self, member: discord.Member):
        await self.log_info(self.log_types["member_join"], member)
        self.print_member_updates("User Joined SERVER '{0}' at {1} - {2}", member)

    async def on_member_remove(self, member: discord.Member):
        await self.log_info(self.log_types["member_leave"], member)
        self.print_member_updates("User Left SERVER '{0}' at {1} - {2}", member)

    async def on_voice_state_update(self, before: discord.Member, after: discord.Member):
        if before.voice.voice_channel is None and after.voice.voice_channel is not None:
            await self.log_info(self.log_types["voice_join"], after)
            self.print_member_updates("User Joined VC in '{0}' at {1} - {2}", after)

        if before.voice.voice_channel is not None and after.voice.voice_channel is None:
            await self.log_info(self.log_types["voice_leave"], after)
            self.print_member_updates("User Left VC in '{0}' at {1} - {2}", after)

    async def log_info(self, logging_type, member: discord.Member):
        time = "Done at {} EST".format(str(datetime.now(pytz.timezone('EST')) + timedelta(hours=1))[:-13])
        description = "{} (ID: {})".format(member.mention, member.id)
        if logging_type == self.log_types["voice_join"]:
            embed = util.make_embed(description=description, author_icon_url=member.avatar_url, footer_text=time,
                                    author_name="User Joined A Voice Chat In '{}'".format(member.server.name),
                                    colour=util.colour_voice)
            await self.send_log(embed=embed)
        elif logging_type == self.log_types["voice_leave"]:
            embed = util.make_embed(description=description, author_icon_url=member.avatar_url, footer_text=time,
                                    author_name="User Left A Voice Chat In '{}'".format(member.server.name),
                                    colour=util.colour_voice)
            await self.send_log(embed=embed)
        elif logging_type == self.log_types["member_join"]:
            embed = util.make_embed(description=description, author_icon_url=member.avatar_url, footer_text=time,
                                    author_name="User Joined Server '{}'".format(member.server.name),
                                    colour=util.colour_join)
            await self.send_log(embed=embed)

        elif logging_type == self.log_types["member_leave"]:
            embed = util.make_embed(description=description, author_icon_url=member.avatar_url, footer_text=time,
                                    author_name="User Left Server '{}'".format(member.server.name),
                                    colour=util.colour_leave)
            await self.send_log(embed=embed)

    async def send_log(self, embed=None):
        try:
            await self.parent_client.send_message(self.temporary_channel, embed=embed)
        except discord.NotFound:
            print("Channel '{}' probably doesn't exist.".format(self.temporary_channel.id))
        except discord.Forbidden:
            print("Client doesn't have permission to send a message in '{}'.".format(self.temporary_channel.id))
        except discord.InvalidArgument:
            print("'temporary_channel' is None, channel doesnt exist")
