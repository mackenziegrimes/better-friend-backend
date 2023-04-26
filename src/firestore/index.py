from google.cloud import firestore
from flask import current_app
from flask.globals import g
from typing import Optional


def get_db() -> firestore.Client:
    if "db" not in g:
        # get project_id from Flask global cache
        project_id: Optional[str] = current_app.config.get("PROJECT_ID")
        # project_id: Optional[str] = g.get("project_id")

        if project_id is not None:
            g.db = firestore.Client(project=project_id)

    return g.db


# @current_app.teardown_appcontext()
def teardown_db(exception):
    db: firestore.Client = g.pop("db", None)

    if db is not None:
        db.close()
