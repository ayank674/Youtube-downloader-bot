import os


class Config:
    OWNER = os.environ['OWNER']

    SESSION_NAME = os.environ['SESSION_NAME']

    API_ID = os.environ['API_ID']

    API_HASH = os.environ['API_HASH']

    BOT_TOKEN = os.environ['BOT_TOKEN']

    CRASH_MESSAGE = os.environ['CRASH_MESSAGE']

    ENCRYPT_KEY = bytes(os.environ['ENCRYPT_KEY'], encoding='utf-8')
