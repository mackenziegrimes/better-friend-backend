from flask import Blueprint, current_app, Response
from typing import Optional, Sequence

from ...firestore import User, get_db

bp = Blueprint("users", __name__)


@bp.route("", methods=["GET"])
async def get_all_users() -> Optional[Sequence[User]]:
    # TODO [nice to have]: return user IDs in response body
    users: list = [user.to_dict() for user in get_db().collection("users").get()]

    current_app.logger.info(f"Query returned users: {users}")
    return {"users": users}


@bp.route("", methods=["POST"])
async def create_user() -> Optional[User]:
    # TODO actually create person
    return {"id": 12345, "name": "new user"}


@bp.route("/<string:id>", methods=["GET"])
async def get_user(id: str) -> Optional[User]:
    current_app.logger.debug(f"Now getting user ID {id}")
    try:
        user = get_db().collection("users").document(id).get().to_dict()
        current_app.logger.info(f"Found user: {user}")

        if user is None:
            return Response(status=404)
        return user
    except Exception as e:
        current_app.logger.warn(f"Failed to get user id {id}: {e}")
        return Response(status=400)


# TODO add support for patch and delete user
