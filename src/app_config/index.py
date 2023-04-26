import os
from dotenv import load_dotenv


class AppConfig(dict):
    PROJECT_ID: str
    GOOGLE_APPLICATION_CREDENTIALS: str
    API_KEY: str

    def __init__(self):
        # load environment variables from .env
        load_dotenv("../../.env")

        # GCP
        self.API_KEY = os.getenv("API_KEY")
        self.PROJECT_ID = os.getenv("PROJECT_ID")
        self.GOOGLE_APPLICATION_CREDENTIALS = os.getenv(
            "GOOGLE_APPLICATION_CREDENTIALS"
        )
