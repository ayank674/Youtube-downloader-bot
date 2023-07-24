from Utubebot import Utubebot
from config import Config

plugins = dict(root='plugins')
Utubebot(Config.SESSION_NAME, api_id=Config.API_ID,
         api_hash=Config.API_HASH, bot_token=Config.BOT_TOKEN, plugins=plugins).run()
