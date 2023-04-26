from flask import Blueprint
from asyncio import sleep
from typing import Optional, Sequence

from ...firestore import Connection
from ..persons import bp as persons_bp

bp = Blueprint("connections", __name__) # TODO can this be cleaned up?


# TODO: add queryString param userId
@persons_bp.route("/<string:id>/connections", methods=["GET"])
def get_all_connections() -> Optional[Sequence[Connection]]:
    # TODO actually get persons
    return {"connections": []}


@persons_bp.route("/<string:id>/connections", methods=["POST"])
def create_connect() -> Optional[Connection]:
    # TODO actually create connection
    connection = { 
        "id": '12345', 
        "personId": 'personId123', 
        "date": '2023-04-23T00:00:01Z',
    }
    return connection


@bp.route("/<string:person_id>/connections/<string:connection_id>", methods=["GET"])
async def get_connection(person_id: str, connection_id: str) -> Optional[Connection]:
    print(f"Now getting connection_id {connection_id} under person_id {person_id}")

    # TODO get connection
    await sleep(0.01)
    connection = {
        "id": connection_id,
        "personId": person_id,
        "date": "2023-04-23T00:00:01Z",
    }

    print(f"Found connection: {connection}")
    return connection

# TODO support delete
async def delete_connection(person_id: str, connection_id: str) -> bool:
    print(f"Now deleting connection_id {connection_id} under person_id {person_id}")

    await sleep(0.01)
    return True
