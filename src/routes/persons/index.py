from asyncio import sleep
from quart import Blueprint, current_app, Request, request, Response
from typing import Optional, Sequence

from google.cloud.firestore import DocumentReference, CollectionReference

from ...firestore import Connection, Person, Firestore

# from ..connections import bp as connections_bp


bp = Blueprint("persons", __name__)
# TODO does this construct the persons/:personId/connections url?
# bp.register_blueprint(connections_bp)


# utilities
def get_collection() -> CollectionReference:
    db = Firestore().db
    return db.collection("users")


def get_user_reference(user_id: str) -> Optional[DocumentReference]:
    user_reference: DocumentReference = get_collection().document(user_id)

    if not user_reference.get().exists:
        return None

    return user_reference


@bp.route("", methods=["GET"])
async def get_all_persons() -> Optional[Sequence[Person]]:
    queryParams = request.args

    if "userId" not in queryParams:
        return Response(
            "Missing required parameter userId",
            status=400,
        )

    user_id = queryParams["userId"]

    try:
        user_reference: Optional[DocumentReference] = get_user_reference(user_id)

        if user_reference is None:
            return Response("User not found", status=400)

        user_collections: Sequence[CollectionReference] = user_reference.collections()

        persons: Sequence[dict] = []
        for collection in user_collections:
            for doc in collection.stream():
                person = doc.to_dict()
                person["id"] = doc.id
                persons.push(person)

        return {"persons": persons}
    except Exception as e:
        current_app.logger.error(f"Failed to get persons for user id {user_id}: {e}")
        return Response("Internal server error", status=500)


@bp.route("", methods=["POST"])
async def create_person() -> Optional[Person]:
    data = await request.get_json()
    current_app.logger.info(f"Attempting to create person with body {data}")

    # TODO validate request body
    if "userId" not in data:
        return Response("Missing required parameter userId", status=400)

    user_id: str = data["userId"]
    del data["userId"]

    user_reference: Optional[DocumentReference] = get_user_reference(user_id)
    if user_reference is None:
        return Response("User not found", status=400)

    try:
        # TODO fails with "expected st instance, dict found"
        person_reference: DocumentReference = user_reference.collection(
            "persons"
        ).document(data)

        current_app.logger.debug(f"Created person id {person_reference.id}")
        return person_reference.get().to_dict()
    except Exception as e:
        current_app.logger.error(f"Failed to create person for userId {user_id}: {e}")
        return Response("Internal server error", status=500)


@bp.route("/<string:id>", methods=["GET"])
async def get_person(id: str) -> Optional[Person]:
    print(f"Now getting person ID {id}")

    # TODO get person
    await sleep(0.01)
    person = {"id": id, "name": "new person"}

    print(f"Found person: {person}")
    return person
