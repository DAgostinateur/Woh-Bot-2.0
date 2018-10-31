class UserAdmin:
    def __init__(self, user_id, server_id):
        self.user_id = user_id
        self.server_id = server_id

    def __eq__(self, other):
        return self.user_id == other.user_id and other.server_id == self.server_id
