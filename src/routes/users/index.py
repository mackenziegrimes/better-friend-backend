from flask import Blueprint
from typing import Optional, Sequence

from asyncio import sleep

bp = Blueprint("users", __name__)

class User():
    id: str
    email: str
    firstName: str
    lastName: str

# TODO connection to DB
@bp.route("", methods=["GET"])
async def get_all_users() -> Optional[Sequence[User]]:
    # TODO actually get persons
    return {"users": []}


@bp.route("", methods=["POST"])
async def create_user() -> Optional[User]:
    # TODO actually create person
    return {"id": 12345, "name": "new user"}


@bp.route("/<string:id>", methods=["GET"])
async def get_user(id: str) -> Optional[User]:
    print(f"Now getting user ID {id}")

    # TODO get person
    await sleep(0.01)
    user = {
        "id": id, 
        "firstName": "John", 
        "lastName": "Smith", 
        "email": "john.smith@domain.com",
    }

    print(f"Found user: {user}")
    return user
