'''Command to unauthenticate a user and prevent him/her from using this bot.'''
from pyrogram import filters
from Utubebot import Utubebot
import helpers


@Utubebot.on_message(filters.command('remove_user') & filters.private)
def remove_user(bot: Utubebot, message):
    try:
        if helpers.msg_handle.check_role(bot, message, 'owner'):
            msg = helpers.msg_handle.extract_msg(message)
            id = helpers.msg_handle.check_id(bot, msg)
            if id:
                bot.user_data.del_user(msg.text)
                bot.send_message(
                    message.chat.id, f"✔️ Successfully removed **{msg.text}**!")
    except:
        helpers.msg_handle.handle_exception(bot, message.chat.id)
