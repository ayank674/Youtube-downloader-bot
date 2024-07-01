'''Store users' data.'''
from config import Config
import psycopg, psycopg.conninfo

class User_data:

    def __init__(self) -> None:
        '''
A python class to store the information of all the users' data in json format. This would store data even if the program crashes.

Basic conventions for role in this class:

all: 
int specified role is 0. There's no restriction on who can use.

owner: 
int specified role is 1. He can use all the commands.

admin:
int specified role is 2. He can use all the commands except removing or changing role of a fellow admin.

user:
int specified role is 3. He can use only the download command.
'''
        
        conn_dict =  psycopg.conninfo.conninfo_to_dict(Config.PG_URI)
        self.conn: psycopg.Connection = psycopg.connect(**conn_dict)
        self.cur = self.conn.cursor()

        self.cur.execute("CREATE TABLE IF NOT EXISTS utube_user_data(ID INT PRIMARY KEY, ROLE INT)")

    def add_user(self, user: str, role: int) -> None:
        '''Function to add a new user to the data or change the role of an exisiting user.'''
        if user.lower() == "all":
            user = 0
        else:
            user = int(user)
        self.cur.execute("INSERT INTO utube_user_data(ID, ROLE) VALUES(%s,%s) ON CONFLICT(ID) DO UPDATE SET ID = EXCLUDED.ID, ROLE = EXCLUDED.ROLE", (user, role))
        self.conn.commit()

    def del_user(self, user: str) -> None:  # Delete a user from json data.
        '''Unauthenticate a user from the bot.'''
        self.cur.execute("DELETE FROM utube_user_data WHERE  = %s", (user,))
        self.conn.commit()

    def show_admins(self) -> str:  # A function to show admins from data.
        '''Returns a list of all the admins.'''
        self.cur.execute("SELECT ID FROM utube_user_data WHERE ROLE = %s", (2,))
        admins = self.cur.fetchall()
        admin_str = ''
        sr_no = 1
        for admin in admins:
            if admin: # Not an empty tuple
                admin_str = admin_str + f'\n**{sr_no}**. {admin[0]}'
                sr_no += 1
        return admin_str

    def show_users(self) -> str:  # A function to show users from data.
        '''Returns a list of all the user. admins are marked in bold.'''
        self.cur.execute("SELECT ID, ROLE FROM utube_user_data WHERE ROLE>%s", (1,)) # Don't include owner
        users = self.cur.fetchall()
        user_str = ''
        sr_no = 1
        for user, role in users:

            if role == 2:  # Display admins in bold.
                user_str = user_str + f'\n{sr_no}. **__{user}__**'

            else:
                user_str = user_str + f'\n{sr_no}. {user}'
            sr_no += 1
        return user_str

    def get_role(self, id):
        '''Returns the role of a user. If user is not authenticated, 4 is returned as role.'''
        id = int(id)
        # Checking if everyone is allowed.
        self.cur.execute("SELECT ROLE FROM utube_user_data WHERE ID = %s", (0,)
        if self.cur.fetchone():
            return 0
        self.cur.execute("SELECT ROLE FROM utube_user_data WHERE ID = %s", (id,))
        role = self.cur.fetchall()
        if role: # A non-empty string if id exists.
            return role[0][0] # return the first element (role) from first row of list.

        else:
            return 4
