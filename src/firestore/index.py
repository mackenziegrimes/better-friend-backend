from google.cloud import firestore
from google import auth
from flask import current_app
from flask.globals import g
from typing import Optional


def get_db() -> firestore.Client:
    current_app.logger.debug(f"g: {g}")
    if "db" not in g:
        # get project_id from Flask global cache
        credentials, project_id = auth.default()
        current_app.logger.debug(f"Loaded credentials for project_id: {project_id}")

        if type(project_id) is str:
            # TODO this is being invoked but global cache does not have db
            current_app.logger.debug("Now storing firestore.Client in global")

            # TODO send config API KEY as well
            g.db = firestore.Client(project=project_id, credentials=credentials)

    return g.db


# @current_app.teardown_appcontext()
def teardown_db(exception):
    db: firestore.Client = g.pop("db", None)

    if db is not None:
        db.close()
