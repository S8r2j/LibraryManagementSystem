import os
from dotenv import load_dotenv

load_dotenv()   # loads the env variables from .env file to the current enn

class Settings:
    DATABASE_NAME = os.getenv('database')
    DATABASE_PASSWORD = os.getenv('password')
    DATABASE_USER = os.getenv('user')
    DATABASE_HOST = os.getenv('host')
    SECRET_KEY = os.getenv('secret_key')

setting = Settings()