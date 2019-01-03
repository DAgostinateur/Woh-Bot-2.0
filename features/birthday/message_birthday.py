class MessageBirthday:
    default_message = "Do a day today. (Default Message)"

    def __init__(self, server_id, birthday_message):
        if birthday_message is None:
            self.birthday_message = self.default_message
        else:
            self.birthday_message = birthday_message
        self.server_id = server_id

    def __eq__(self, other):
        return self.server_id == other.server_id
