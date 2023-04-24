from flask import Blueprint
from asyncio import sleep
from typing import Optional, Sequence

class Connection():
    id: str
    personId: str
    date: str # TODO date might not be a string

bp = Blueprint("connections", __name__)


# TODO: add queryString param userId
@bp.route("", methods=["GET"])
def get_all_connections() -> Optional[Sequence[Connection]]:
    # TODO actually get persons
    return {"connections": []}


@bp.route("", methods=["POST"])
def create_connect() -> Optional[Connection]:
    # TODO actually create person
    connection = { 
        "id": '12345', 
        "personId": 'personId123', 
        "date": '2023-04-23T00:00:01Z',
    }
    return connection


@bp.route("/<string:id>", methods=["GET"])
async def get_connection(id: str) -> Optional[Connection]:
    print(f"Now getting connection ID {id}")

    # TODO get person
    await sleep(0.01)
    connection = {
        "id": "12345",
        "personId": "personId123",
        "date": "2023-04-23T00:00:01Z",
    }

    print(f"Found connection: {connection}")
    return connection
