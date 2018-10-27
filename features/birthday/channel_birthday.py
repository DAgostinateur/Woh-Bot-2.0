class ChannelBirthday:
    def __init__(self, channel_id, server_id):
        self.channel_id = channel_id
        self.server_id = server_id

    def __eq__(self, other):
        return self.server_id == other.server_id
