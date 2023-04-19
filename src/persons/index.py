from flask import Blueprint

bp = Blueprint("persons", __name__)

@bp.route("", methods=["GET"])
def root():
    # TODO actually return persons
    return {
        "persons": []
    }

@bp.route("", methods=["POST"])
def create_person():
    # TODO actually create person
    return {
        "id": 12345,
        "name": "new person"
    }
