import os


class Config:
    OWNER = os.environ.get("OWNER", 0)

    SESSION_NAME = os.environ.get("SESSION_NAME", "Utube-bot")

    API_ID = os.environ.get("API_ID")

    API_HASH = os.environ.get("API_HASH")

    BOT_TOKEN = os.environ.get("BOT_TOKEN")

    CRASH_MESSAGE = os.environ.get("CRASH_MESSAGE", "Oops! Something went wrong")

    START_MESSAGE = os.environ.get("START_MESSAGE", "Hi! This a bot.")

    PG_URI = os.environ.get("PG_URI")
