'''Functions to handle messages sent by the user to the bot.'''
from typing import Literal
from pyrogram import types
from config import Config
import pytube.exceptions as pyex


# Make sure command is used only by authorised person.
def check_role(bot, message: types.Message, role: Literal['owner', 'admin', 'user']):
    '''
    Check whether the user is authenticated to use a particular command.
    Sends a reply message to the user if is he is not authenticated to a proper role to use this command.
    '''
    role_id = {'owner': 1, 'admin': 2, 'user': 3}
    id = message.chat.id
    user_role = bot.user_data.get_role(id)
    # Checking is bot usage is limited to users.
    if not bot.user_data.restricted and role_id == 3:
        return True
    if user_role <= role_id[role]:
        return True
    else:
        # A dict to see whether to add a/an/the in the reply message.
        a_an_the = {'owner': 'the', 'admin': 'an', 'user': 'a'}
        bot.send_message(
            message.chat.id, f"🚫 You are not {a_an_the[role]} {role}. You can't use this function.")
        return False


def extract_msg(message: types.Message):
    '''
    Check if the user has used a particular command by replying to another message.
    If he has replied, all the data is to be extracted from the latter message.
    '''
    if message.reply_to_message:
        return message.reply_to_message
    else:
        return message


def check_id(bot, message: types.Message):
    '''
    Check if the given message contains only digits (valid id).
    If it isn't a valid id, a reply is sent to the user.
    '''
    if message.text.isdigit() or message.text.lower() == "all":
        return message.text
    else:
        bot.send_message(message.chat.id, f'❌ This is not a valid id!{message.text}')
        return None


def handle_exception(bot, user_id: int):
    '''Sends a message to the user if an unexpected error is occured while executing a particular process.'''
    bot.send_message(user_id, Config.CRASH_MESSAGE)


def handle_utube_exception(bot, user_id: int, exception):
    '''
    Sends appropriate message to the user corresponding to the error that occures during creation of a Youtube object.
    If it isn't a Youtube object creation error, the usual crash message is sent to the user.
    '''
    exceptions = {pyex.AgeRestrictedError: '❗Can\'t download video as it is **AGE RESTRICTED**.',
                  pyex.ExtractError: '❗Unable to extract video **DATA**.',
                  pyex.HTMLParseError: '❗An error occures while parsing **HTML**.',
                  pyex.LiveStreamError: '❗Can\'t download video as it is **LIVE STREAM**.',
                  pyex.MaxRetriesExceeded: '❗**MAX RETRIES EXCEEDED** so can\'t download this video.',
                  pyex.MembersOnly: '❗This video is a **MEMBERS ONLY**',
                  pyex.RegexMatchError: '❗This is not a **YOUTUBE LINK**',
                  pyex.RecordingUnavailable: '❗**RECORDING** is not available',
                  pyex.VideoPrivate: '❗can\'t download **PRIVATE VIDEO**',
                  pyex.VideoRegionBlocked: '❗This video is **REGION BLOCKED**',
                  pyex.VideoUnavailable: '❗This video is **NOT AVAILABLE**'}
    error_message = exceptions.get(type(exception))
    if error_message:
        bot.send_message(user_id, error_message)
    else:
        handle_exception(bot, user_id)
