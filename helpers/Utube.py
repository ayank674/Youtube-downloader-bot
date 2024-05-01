import random as rd
import string
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, Message
from pytube import YouTube
import re
import os
import urllib.request
from . import msg_handle
import utils.converter

download_data = {}


class Utube:
    def __init__(self, link: YouTube, Utubebot, user_id: str) -> None:
        '''
        A class to store all the data of a particular download process.

        Parameters:

        link(``str``) - 
            the yt video's link that is to be downloaded.

        Utubebot(``Utubebot``) - 
            telegram bot that sends message to the user.

        user_id(``int``) - 
            id of the user that initiated the process.
        '''
        self.process_id = self.generate_unique_id()
        self.link = link
        self.messages = utube_messages(Utubebot, user_id, self.process_id)
        self.yt_obj = self.generate_yt_obj()
        if self.yt_obj:
            self.thumbnail = self.get_thumbnail()
            self.register_process()

    def generate_unique_id(self) -> str:
        '''returns a unique id for the process.'''
        characters = list(string.ascii_letters)
        characters.extend(list(string.digits))
        id = ''.join([rd.choice(characters) for _ in range(5)])
        if id in download_data:
            self.generate_unique_id()
        else:
            return id

    def register_process(self):
        '''appends the process id with corresponding user to download data.'''
        download_data[self.process_id] = self

    def generate_yt_obj(self) -> YouTube | None:
        '''Creates a Youtube object from the link.'''
        try:
            yt_object = YouTube(
                self.link, on_progress_callback=self.messages.on_progress)
            return yt_object
        except Exception as exception:
            msg_handle.handle_utube_exception(
                self.messages.Utubebot, self.messages.user_id, exception)
            return None

    def download(self, itag) -> str:
        '''Downloads a stream from the itag.

        Parameter:
        itag(``int``) -
            itag of the stream to be downloaded.
        '''
        self.stream = self.yt_obj.streams.get_by_itag(itag)
        self.type = self.stream.type
        self.file_path = utils.converter.abs_path(f'videos\\{self.process_id}')
        self.file = self.stream.download(output_path=self.file_path)
        if self.stream.type == 'audio':
            new_file = f'{".".join(self.file.split(".")[:-1])}.mp3'
            os.rename(self.file, new_file)
            self.file = new_file
        return self.file

    def get_thumbnail(self) -> str:
        '''Returns a thumbnail path after download the video's thumbnail.'''
        folder = utils.converter.abs_path('thumbnails\\')
        if not os.path.exists(folder):
            os.makedirs(folder)
        thumbnail_path = utils.converter.abs_path(
            f'thumbnails\{self.process_id}.jpg')
        urllib.request.urlretrieve(self.yt_obj.thumbnail_url, thumbnail_path)
        return thumbnail_path

    def remove_files(self):
        '''Removes all the downloaded files after they are uploaded to telegram.'''
        os.remove(self.file)
        os.rmdir(self.file_path)
        os.remove(self.thumbnail)


class utube_messages:
    def __init__(self, Utubebot, user_id: int, process_id: int) -> None:
        '''
        A class to store all the telegram messages sent to the user while download is in progress.

        Parameters:
        Utubebot(``Utubebot``) -
            the bot that sends message to the user.

        user_id(``int``) -
            telegram id of the user that initiated this process.

        process_id(``int``) -
            the id of the process that this object belongs to.
        '''
        self.Utubebot = Utubebot
        self.user_id = user_id
        self.process_id: int = process_id
        self.callback_query: CallbackQuery = None
        self.upload_message: Message = None
        self.file_type: str = None
        self.counter = 0

    def generate_markup_keyboard(self, file_type, yt_obj: YouTube) -> InlineKeyboardMarkup:
        '''Returns an Inline markup keyboard with all the stream options of a Youtube object.'''
        buttons = []
        try:
            
            if file_type == '1':  # user needs both audio and video.
                self.file_type = 'video'
                filtrd_streams = yt_obj.streams.filter(progressive=True)

            elif file_type == '2':  # user needs only video.
                self.file_type = 'video'
                filtrd_streams = yt_obj.streams.filter(
                    adaptive=True, only_video=True)

            elif file_type == '3':  # user nedds only audio.
                self.file_type = 'audio'
                filtrd_streams = yt_obj.streams.filter(only_audio=True)

            for stream in filtrd_streams:
                if stream.filesize_mb > 2000:
                    continue
                button = InlineKeyboardButton(self.generate_button_text(stream),
                                          callback_data=(f'{stream.itag}itag{self.process_id}'))
                buttons.append([button])

            return InlineKeyboardMarkup(buttons)
        except Exception as exception:
            msg_handle.handle_utube_exception(
                self.Utubebot, self.user_id, exception)
            return None
            
    def generate_button_text(self, stream) -> str:
        '''Returns the text of a markup button.'''
        if stream.type == 'video':
            # Parsing through mimie type to get extension of the stream.
            extension_lst = re.findall('/(.*)', stream.mime_type)
            if extension_lst:
                extension = extension_lst[0]
                return f'🎞️ {extension},{round(stream.filesize_mb,2)}mb,{stream.resolution}'
            else:  # If regex isn't matched, return text without extension.
                return f'🎞️ {round(stream.filesize_mb,2)}mb,{stream.resolution}'
        # Audios are converted to mp3 so there's no use of extension.
        if stream.type == 'audio':
            return f'🔊 {round(stream.filesize_mb,2)}mb,{stream.abr}'

    def on_progress(self, stream, file, bytes_remaining):
        '''Sends a progress bar type message when file is downloading..'''
        self.title = stream.title
        total = round(stream.filesize_mb, 2)
        mb_remaining = round(bytes_remaining/(1048576), 2)
        done = round(total - mb_remaining, 2)
        percent = round(100*(done)/total, 2)
        filled_boxes = int(percent//10)
        empty_boxes = 10 - filled_boxes
        progress_bar = '■'*filled_boxes + '□'*empty_boxes
        progress_message = ''.join([f'**Title**: __{self.title}__\n\n',
                                    f'⚙️ **Processed**: [{progress_bar}]',
                                    f' {percent}%\n\n', f'📦 **Downloaded**: {done}MB of {total}MB'])
        self.callback_query.edit_message_caption(progress_message)

    def upload_file(self, thumbnail: str, file: str):
        '''Upload file to the user'''
        if self.file_type == 'video':
            self.Utubebot.send_video(
                self.user_id, file, f'**{self.title}**', thumb=thumbnail, supports_streaming=True, progress=self.on_upload)
        elif self.file_type == 'audio':
            self.Utubebot.send_audio(
                self.user_id, file, f'**{self.title}**', thumb=thumbnail, progress=self.on_upload)

    def on_upload(self, current, total):
        '''Sends a progress bar type message when file is being uploaded to the user.'''
        self.counter += 1
        if self.counter % 5 != 0:
            return
        current_mb = round(current/1048576, 2)
        total_mb = round(total/1048576, 2)
        percent = round((100*(current_mb))/total_mb, 2)
        filled_boxes = int(percent//10)
        empty_boxes = 10 - filled_boxes
        progress_message = ''.join([f'**Title**: __{self.title}__\n\n',
                                    f'⚙️ **Processed**: [{"■"*filled_boxes}{"□"*empty_boxes}]',
                                    f' {percent}%\n\n', f'📦 **Uploaded**: {current_mb}MB of {total_mb}MB'])
        self.upload_message.edit_caption(progress_message)
