"""Module for interacting with Google Firestore database"""
from google.cloud.firestore import Client, CollectionReference
from google import auth
from quart import current_app, Config
from typing import Optional

from src.app_config import AppConfig


class Firestore:
    """Firestore database connection instance"""
    def __init__(self):
        app_config: Config = current_app.config
        credentials, project_id = auth.load_credentials_from_file(
            app_config.get("GOOGLE_APPLICATION_CREDENTIALS")
        )

        if isinstance(project_id, str):
            self.db = Client(
                project=project_id,
                credentials=credentials,
                client_info={"api_key": app_config.get("API_KEY")},
            )

    # @current_app.teardown_appcontext()
    def teardown(self):
        """Cleanly shutdown db connection"""
        if self.db is not None:
            self.db.close()

    @staticmethod
    def get_collection() -> CollectionReference:
        """
        Utility function to get current Firestore instance and the base Users 
        collection under which everything lives.
        Note that this must be called from within a Quart request context.
        """
        db = Firestore().db
        return db.collection("users")
