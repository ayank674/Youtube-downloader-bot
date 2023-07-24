from helpers import user_data
from pyrogram import Client
from config import Config


class Utubebot(Client):
    '''A bot with additional user_data attribute.'''

    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
        self.user_data = user_data.user_data()
        self.user_data.add_user(Config.OWNER, 1)
