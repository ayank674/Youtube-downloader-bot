'''download - reply to this command with yt link.'''
from pyrogram import filters
from pyrogram.errors import bad_request_400
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from Utubebot import Utubebot
import helpers


@Utubebot.on_message(filters.command('download') & filters.private)
def download(bot: Utubebot, message: Message):
    '''Sends a message to the user asking him to select the type of file he wants to download.'''
    if helpers.msg_handle.check_role(bot, message, 'user'):

        msg = helpers.msg_handle.extract_msg(message)
        link = msg.text

        utube_obj = helpers.Utube.Utube(link, bot, msg.chat.id)
        if not utube_obj.yt_obj:  # The process has failed.
            return None
        process_id = utube_obj.process_id
        # Now formatting reply markup keyboard for user.
        button_both = InlineKeyboardButton(
            '🎞️ Audio and Video both', callback_data=''.join(['1', 'type', process_id]))
        button_video = InlineKeyboardButton(
            '📹 Video Only', callback_data=''.join(['2', 'type', process_id]))
        button_audio = InlineKeyboardButton(
            '🔊 Audio Only', callback_data=''.join(['3', 'type', process_id]))
        buttons = [[button_audio, button_video], [button_both]]
        keyboard = InlineKeyboardMarkup(buttons)
        bot.send_message(
            message.chat.id, text='**Choose the type of file you want to download**:', reply_markup=keyboard)


@Utubebot.on_callback_query(filters.regex('.*type.*'))
def get_streams(bot: Utubebot, callback_query: CallbackQuery):
    '''Asks the user to select the his desired quality of stream.'''
    try:
        callback_query.edit_message_caption('⚙️ **Processing....**')
    except bad_request_400.MessageNotModified:
        callback_query.answer(
            '❌ Don\'t press the buttons more than once.', show_alert=True)
        return None
    callback_data = callback_query.data.split('type')
    file_type = callback_data[0]
    process_id = callback_data[1]
    Utube_obj: helpers.Utube.Utube = helpers.Utube.download_data[process_id]
    markup_keyboard = Utube_obj.messages.generate_markup_keyboard(
        file_type, Utube_obj.yt_obj)
    if markup_keyboard is None:
        bot.delete_messages(callback_query.message.chat.id, callback_query.id)
        return
    callback_query.edit_message_caption(
        '**Choose the resolution of your desired file**:', reply_markup=markup_keyboard)


@Utubebot.on_callback_query(filters.regex('.*itag.*'))
def dl_file(bot: Utubebot, callback_query: CallbackQuery):
    '''Downloads and uploads the file.'''
    try:
        callback_query.edit_message_caption('**Initiating Download......**')
    except bad_request_400.MessageNotModified:
        callback_query.answer(
            '❌ Don\'t press the buttons more than once.', show_alert=True)
        return None
    callback_data = callback_query.data.split('itag')
    itag = callback_data[0]
    process_id = callback_data[1]
    Utube_obj: helpers.Utube.Utube = helpers.Utube.download_data[process_id]
    Utube_obj.messages.callback_query = callback_query
    Utube_obj.download(int(itag))
    bot.delete_messages(Utube_obj.messages.user_id,
                        Utube_obj.messages.callback_query.message.id)
    Utube_obj.messages.upload_message = bot.send_message(
        Utube_obj.messages.user_id, '**Uploading....**')
    Utube_obj.messages.upload_file(Utube_obj.thumbnail, Utube_obj.file)
    bot.delete_messages(
        Utube_obj.messages.user_id, Utube_obj.messages.upload_message.id)
    Utube_obj.remove_files()
