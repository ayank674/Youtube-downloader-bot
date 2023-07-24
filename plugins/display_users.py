'''
display_users - show the list of authenticated users for this bot.
display_admins - show the list of authenticated admins for this bot.
'''
from pyrogram import filters
from Utubebot import Utubebot
import helpers


@Utubebot.on_message(filters.command('display_users'))
def display_users(bot: Utubebot, message):
    try:
        if helpers.msg_handle.check_role(bot, message, 'admin'):
            users = bot.user_data.show_users()
            if users:
                bot.send_message(
                    message.chat.id, f"**Here's the list of users**:{users}")
            else:
                bot.send_message(message.chat.id, '❌ There are no users yet!')
    except:
        helpers.msg_handle. handle_exception(bot, message.chat.id)


@Utubebot.on_message(filters.command('display_admins'))
def display_admins(bot: Utubebot, message):
    try:
        if helpers.msg_handle.check_role(bot, message, 'owner'):
            admins = bot.user_data.show_admins()
            if admins:
                bot.send_message(
                    message.chat.id, f"**Here's the list of admins**:{admins}")
            else:
                bot.send_message(message.chat.id, '❌ There are no admins yet!')
    except:
        helpers.msg_handle.handle_exception(bot, message.chat.id)
