from asyncio import sleep
from flask import Blueprint
from typing import Optional, Sequence

from ..connections import bp as connections_bp, Connection


class Person:
    id: str
    name: Optional[str]
    type: str
    frequencyDays: int


bp = Blueprint("persons", __name__)
# TODO does this construct the persons/:personId/connections url?
bp.register_blueprint(connections_bp) 


# TODO: add queryString param userId
@bp.route("", methods=["GET"])
def get_all_persons() -> Optional[Sequence[Person]]:
    # TODO actually get persons
    return {"persons": []}


@bp.route("", methods=["POST"])
def create_person() -> Optional[Person]:
    # TODO actually create person
    return {"id": "12345", "name": "new person"}


@bp.route("/<string:id>", methods=["GET"])
async def get_person(id: str) -> Optional[Person]:
    print(f"Now getting person ID {id}")

    # TODO get person
    await sleep(0.01)
    person = {"id": id, "name": "new person"}

    print(f"Found person: {person}")
    return person
