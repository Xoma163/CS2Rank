import json
import os


class Users:
    """
    Cache latest's user games in temp file
    """
    USERS_FILE = 'users.json'

    def __init__(self):
        self.users = {}
        self.read()

    def set_code(self, steam_id: int, code: str):
        self.users[steam_id]['share_code'] = code

    def read(self):
        if os.path.exists(self.USERS_FILE):
            with open(self.USERS_FILE, 'r') as file:
                self.users = json.load(file)
        self.users = {int(x): self.users[x] for x in self.users}

    def write(self):
        with open(self.USERS_FILE, 'w') as file:
            data = json.dumps(self.users, indent=2)
            file.write(data)
