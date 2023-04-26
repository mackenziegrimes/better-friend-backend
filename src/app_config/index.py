import os
from dotenv import load_dotenv


class AppConfig(dict):
    DB_PORT: str
    DB_HOSTNAME: str
    DB_USERNAME: str
    DB_PASSWORD: str
    PROJECT_ID: str

    def __init__(self):
         # load environment variables from .env
        load_dotenv("../../.env")
        
        self.DB_PORT = os.getenv("DB_PORT")
        self.DB_HOSTNAME = os.getenv("DB_HOSTNAME")
        self.DB_USERNAME = os.getenv("DB_USERNAME")
        self.DB_PASSWORD = os.getenv("DB_PASSWORD")

        self.PROJECT_ID = os.getenv("PROJECT_ID")
