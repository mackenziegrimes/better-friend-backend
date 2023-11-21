"""Health route business module"""
from quart import Blueprint, abort, current_app
from src.firestore import Firestore

bp = Blueprint("main", __name__)
# pylint: disable=broad-exception-caught



@bp.route("", methods=["GET"])
def index():
    """Base /health endpoint"""
    try:
        db = Firestore().db
        users = db.collection("users").count().get()
        current_app.logger.info(f"User count: {(len(users))}")

        if users is not None and len(users) > 0:
            return {"status": "OK"}

        raise RuntimeError("No collections found in Firestore")

    except Exception as e:
        current_app.log_exception(f"Failed to connection to Firestore: {e}")
        abort(500, description="Internal Server Error")
