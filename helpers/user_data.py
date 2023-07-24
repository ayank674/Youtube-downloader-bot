'''Store users' data.'''
import json
from config import Config
import utils.converter
from cryptography.fernet import Fernet
import os

fernet = Fernet(Config.ENCRYPT_KEY)


class user_data:

    def __init__(self) -> None:
        '''
A python class to store the information of all the users' data in json format. This would store data even if the program crashes.

Basic conventions for role in this class:

owner: 
int specified role is 1. He can use all the commands.

admin:
int specified role is 2. He can use all the commands except removing or changing role of a fellow admin.

user:
int specified role is 3. He can use only the download command.


JSON is stored in following format:

{"Users": {"User1": {"role": int}, {"User2": {"role": int},.....}}
'''
        if not os.path.isfile(utils.converter.abs_path('user_data.json')):
            # Create a new dict if no previous data is there.
            self.data: json = json.loads('{"users":{}}')

        else:
            with open(utils.converter.abs_path('user_data.json'), 'rb') as f:
                self.data: json = json.loads(fernet.decrypt(f.read()))

        self.users: dict = self.data['users']

    def add_user(self, user: str, role: int) -> None:
        '''Function to add a new user to the data.'''
        self.users[str(user)] = {'role': role}
        write_file('user_data.json', self.data)

    def del_user(self, user: str) -> None:  # Delete a user from json data.
        '''Unauthenticate a user from the bot.'''
        self.users.pop(str(user), None)
        write_file('user_data.json', self.data)

    def change_role(self, user: str, new_role: int) -> None:
        '''Change the role of an admin/user to an admin/user.'''
        if self.users.get(str(user)):
            self.users[str(user)]['role'] = new_role
        else:
            self.users[str(user)] = {'role': new_role}  # It is a new user.
        write_file('user_data.json', self.data)

    def show_admins(self) -> str:  # A function to show admins from data.
        '''Returns a list of all the admins.'''
        admin_str = ''
        sr_no = 1
        for user in self.users:
            role = self.users[user].get('role')
            if role == 2:  # The user is an admin.
                admin_str = admin_str + f'\n**{sr_no+1}**. {user}'
                sr_no += 1
        return admin_str

    def show_users(self) -> str:  # A function to show users from data.
        '''Returns a list of all the user. admins are marked in bold.'''
        user_str = ''
        sr_no = 1
        for user in self.users:
            role = self.users[user].get('role')
            if role == 1:  # Don't include owner in list.
                continue

            elif role == 2:  # Display admins in bold.
                user_str = user_str + f'\n{sr_no+1}. **__{user}__**'

            else:
                user_str = user_str + f'\n{sr_no+1}. {user}'
            sr_no += 1
        return user_str

    def get_role(self, id):
        '''Returns the role of a user. If user is not authenticated, 4 is returned as role.'''
        if self.users.get(str(id)):
            return self.users[str(id)].get('role')

        else:
            return 4


def write_file(relpath: str, js: json):
    '''Function to write the dict to a new file in json format.'''
    path = utils.converter.abs_path(relpath)
    with open(path, 'wb') as f:
        # JSON only allows double quotes.
        str_data = json.dumps(js)
        f.write(fernet.encrypt(bytes(str_data, encoding='utf-8')))
