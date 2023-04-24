from flask import Blueprint
from typing import Optional, Sequence


class Person:
    id: str
    name: Optional[str]


bp = Blueprint("persons", __name__)


@bp.route("", methods=["GET"])
def get_all_persons() -> Optional[Sequence[Person]]:
    # TODO actually get persons
    return {"persons": []}


@bp.route("", methods=["POST"])
def create_person() -> Optional[Person]:
    # TODO actually create person
    return {"id": 12345, "name": "new person"}


@bp.route("/<string:id>", methods=["GET"])
async def get_person(id: str) -> Optional[Person]:
    print(f"Now getting person ID {id}")

    # TODO get person
    await sleep(0.01)
    person = {"id": id, "name": "new person"}

    print(f"Found person: {person}")
    return person
