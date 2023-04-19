from flask import Blueprint

bp = Blueprint('main', __name__)

@bp.route('/health', methods=["GET"])
def index():
    return {
        "status": "OK"
    }
