import discord

import wohbot2


class LoggingHandler(object):

    def __init__(self, client: wohbot2.WohBot):
        self.parent_client = client

        self.main_log_channel = None
