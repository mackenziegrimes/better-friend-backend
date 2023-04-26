from flask import Blueprint, abort, current_app
from ...firestore import get_db

bp = Blueprint("main", __name__)


@bp.route("", methods=["GET"])
def index():
    try:
        collections = get_db().collection("users").count().get()
        print(f"Collections: {(collections.count)}")

        if collections is not None and collections.count > 0:
            return {"status": "OK"}
        else:
            raise Exception("No collections found in Firestore")

    except Exception as e:
        current_app.log_exception(f"Failed to connection to Firestore: {e}")
        abort(500, description="Internal Server Error")
