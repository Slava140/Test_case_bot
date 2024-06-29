import os

from dotenv import load_dotenv
from pathlib import Path

env_file_path = Path(__file__).parent.parent/'.env'
load_dotenv(env_file_path)


class Settings:
    def __init__(self):
        self.BOT_TOKEN = os.environ.get('BOT_TOKEN')
        self.API_URL = os.environ.get('API_URL')


settings = Settings()
