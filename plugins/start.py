'''Start command with a welcome message. This is used to verify that bot is online.'''
from pyrogram import filters
from Utubebot import Utubebot


@Utubebot.on_message(filters.command('start') & filters.private)
def start(bot: Utubebot, message):
    if message.chat.username:
        name = message.chat.username.capitalize()
    else:
        name = ''
    bot.send_message(
        message.chat.id, f"👋 **Hi {name}**!\n\n• __This is a simple bot to download youtube videos__.\n\n• **To Use**: __Send a youtube video link and reply to it with /download command__.\n\n• **Disclaimer**: __Do not infringe anyone's copyright using this bot.__")
