from google.cloud import firestore
import google.auth as auth
from quart import current_app, Config
from typing import Optional

from ..app_config import AppConfig


class Firestore:
    db: firestore.Client

    def __init__(self):
        app_config: Config = current_app.config
        credentials, project_id = auth.load_credentials_from_file(
            app_config.get("GOOGLE_APPLICATION_CREDENTIALS")
        )

        if type(project_id) is str:
            self.db = firestore.Client(
                project=project_id,
                credentials=credentials,
                client_info={"api_key": app_config.get("API_KEY")},
            )

    # @current_app.teardown_appcontext()
    def teardown(self):
        if self.db is not None:
            self.db.close()
