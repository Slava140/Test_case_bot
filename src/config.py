import os

from dotenv import load_dotenv
from pathlib import Path

env_file_path = Path(__file__).parent.parent/'.env'
load_dotenv(env_file_path)


class Settings:
    def __init__(self):
        self.BOT_TOKEN = os.environ.get('BOT_TOKEN')
        self.API_URL = os.environ.get('API_URL')
        self.REDIS_HOST = os.environ.get('REDIS_HOST')
        self.REDIS_PORT = os.environ.get('REDIS_PORT')


settings = Settings()
