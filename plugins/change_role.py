'''Command to the the role of a person from admin/user to admin/user.'''

from pyrogram import filters
from Utubebot import Utubebot
from pyrogram.errors import bad_request_400
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
import helpers


@Utubebot.on_message(filters.command('change_role') & filters.private)
def change_role(bot: Utubebot, message):
    try:
        if helpers.msg_handle.check_role(bot, message, 'owner'):
            msg = helpers.msg_handle.extract_msg(message)
            id = helpers.msg_handle.check_id(bot, msg)
            if id:
                change_role_options = [[InlineKeyboardButton('👨‍🔧 Admin', callback_data=str(2) + f'/{msg.text}' + 'role'),
                                        InlineKeyboardButton('👨‍💻 User', callback_data=str(3) + f'/{msg.text}' + 'role')]]
                keyboard = InlineKeyboardMarkup(change_role_options)

                # Send message with buttons to select role as admins or user.
                bot.send_message(
                    message.chat.id, text=f'**Choose the role you want to change {msg.text} to**:', reply_markup=keyboard)
    except:
        helpers.msg_handle.handle_exception(bot, message.chat.id)


@Utubebot.on_callback_query(filters.regex('.*role'))
def final_change_role(bot: Utubebot, callback_query: CallbackQuery):
    try:
        callback_data: str = callback_query.data.removesuffix('role')
        # parse through the callback data to extract its content and change the role of the mentioned user.
        callback_data_req = callback_data.split('/')
        new_role = int(callback_data_req[0])
        change_role_user = callback_data_req[1]
        # dict mentioning the no. to its corresponding role.
        id_to_role = {'2': 'admin', '3': 'user'}
        reply = f'✔️ Successfully changed the role of **{change_role_user}** to {id_to_role[str(new_role)]}'
        try:
            bot.user_data.change_role(change_role_user, new_role)
            callback_query.edit_message_caption(reply)
        except bad_request_400.MessageNotModified:
            # This means user has clicked the button twice..
            callback_query.answer(
                '❌ Don\'t press the buttons more than once.', show_alert=True)
    except:
        helpers.msg_handle.handle_exception(
            bot, callback_query.message.chat.id)
