import discord
import os
import json

import util
from features.admin import user_admin


class AdminHandler(object):
    user_admin_file = "data/user_admin.json"

    json_user_id = "user_id"
    json_server_id = "server_id"

    def __init__(self, client):
        self.parent_client = client

        self.user_admins = self.get_user_admins()

    def _write_to_admin_file(self):
        info_dicts = [{self.json_user_id: x.user_id, self.json_server_id: x.server_id} for x in
                      self.user_admins]
        json_string = json.dumps(info_dicts, indent=4, separators=(',', ' : '))
        with open(self.user_admin_file, 'w') as file:
            file.write(json_string)

    def is_user_admin(self, user_id, server_id):
        return self.get_user_admin(user_id, server_id) is not None

    def get_admin_count(self, server: discord.Server):
        count = 0
        for admin in self.user_admins:
            if admin.server_id == server.id and server.get_member(admin.user_id) is not None:
                count += 1
        return count

    def get_user_admin(self, user_id, server_id):
        """Returns a UserAdmin with a user id and server id

        :param user_id:
        :param server_id:
        :return: UserAdmin
        """
        for admin in self.user_admins:
            if admin.user_id == user_id and server_id == admin.server_id:
                return admin
        return None

    def get_user_admins(self):
        if not os.path.exists(self.user_admin_file):
            util.check_file(self.user_admin_file)
            return []

        with open(self.user_admin_file, 'r') as file:
            if os.stat(self.user_admin_file).st_size == 0:
                return []

            user_admin_list = []
            for d in json.load(file):
                try:
                    user_admin_list.append(
                        user_admin.UserAdmin(d[self.json_user_id], d[self.json_server_id]))
                except KeyError:
                    print("user_id or server_id doesnt exist: {}".format(d))

            return user_admin_list

    def save_user_admin(self, user_id, server_id):
        self.user_admins.append(user_admin.UserAdmin(user_id, server_id))
        print("SUCCEEDED to add user admin.")
        self._write_to_admin_file()

    def remove_user_admin(self, user_id, server_id):
        try:
            self.user_admins.remove(self.get_user_admin(user_id, server_id))
        except ValueError:
            print("FAILED to remove user admin.")
            return

        self._write_to_admin_file()

        print("SUCCEEDED to remove user admin.")
