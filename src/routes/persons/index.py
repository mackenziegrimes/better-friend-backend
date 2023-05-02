from quart import Blueprint, current_app, Request, request, Response
from datetime import datetime
from typing import Optional, Sequence

from google.cloud.firestore import (
    DocumentReference,
    CollectionReference,
    DocumentSnapshot,
)

from ...firestore import Connection, Person, get_collection

bp = Blueprint("persons", __name__)


def get_user_reference(user_id: str) -> Optional[DocumentReference]:
    user_reference: DocumentReference = get_collection().document(user_id)
    return user_reference if user_reference.get().exists else None


@bp.route("", methods=["GET"])
async def get_all_persons(user_id: str) -> Optional[Sequence[Person]]:
    try:
        user_reference: Optional[DocumentReference] = get_user_reference(user_id)
        if user_reference is None:
            return Response("User not found", status=400)

        # loop through persons DocumentReferences and build Person model object
        user_collections: Sequence[CollectionReference] = user_reference.collections()
        persons: Sequence[dict] = []
        for collection in user_collections:
            for doc in collection.stream():
                person = doc.to_dict()
                person["id"] = doc.id
                persons.append(person)

        return {"persons": persons}
    except Exception as e:
        current_app.logger.error(f"Failed to get persons for user id {user_id}: {e}")
        return Response("Internal server error", status=500)


@bp.route("", methods=["POST"])
async def create_person(user_id: str) -> Optional[Person]:
    data = await request.get_json()
    current_app.logger.info(f"Creating person for user {user_id} with body: {data}")

    # TODO validate request body
    user_reference: Optional[DocumentReference] = get_user_reference(user_id)
    if user_reference is None:
        return Response("User not found", status=404)

    current_app.logger.debug(f"User reference id: {user_reference.id}")

    try:
        # create new person document in persons subcollection under this user
        person_reference: CollectionReference = user_reference.collection("persons")
        person_doc: DocumentReference = person_reference.document()
        person_doc.create(data)

        # append the id to the rest of the data before returning
        person_data: dict = person_doc.get().to_dict()
        person_data["id"] = person_doc.id

        current_app.logger.info(f"Created person: {person_data}")
        return person_data
    except Exception as e:
        current_app.logger.error(f"Failed to create person for userId {user_id}: {e}")
        return Response("Internal server error", status=500)


@bp.route("<string:person_id>", methods=["GET"])
async def get_person(user_id: str, person_id: str) -> Optional[Person]:
    current_app.logger.info(f"Getting person_id {person_id} from user {user_id}")

    # get base User document which has persons nested collection, if it exists
    user_reference: Optional[DocumentReference] = get_user_reference(user_id)
    if user_reference is None:
        return Response(status=404)

    # attempt to get Person Document, if one by this id exists
    person_snapshot: DocumentSnapshot = (
        user_reference.collection("persons").document(person_id).get()
    )
    if not person_snapshot.exists:
        return Response(status=404)

    person = person_snapshot.to_dict()
    person["id"] = person_snapshot.id
    return person


@bp.route("<string:person_id>", methods=["PATCH"])
async def patch_person(user_id: str, person_id: str):
    request_body: dict = await request.get_json()
    current_app.logger.info(f"Now updating person {person_id} with body {request_body}")

    # get base User document which has persons nested collection, if it exists
    user_reference: Optional[DocumentReference] = get_user_reference(user_id)
    if user_reference is None:
        return Response(status=404)

    # only send fields that we consider updatable
    sanitized_body: dict = {}
    for field in ["firstName", "lastName", "relationshipType", "frequencyDays"]:
        if field in request_body:
            sanitized_body[field] = request_body[field]

    sanitized_body["updatedAt"] = datetime.utcnow()

    try:
        person_doc: DocumentReference = user_reference.collection("persons").document(
            person_id
        )
        person_doc.update(sanitized_body)

        # Construct Person model object and return
        updated_person: dict = person_doc.get().to_dict()
        updated_person["id"] = person_doc.id

        return updated_person

    except Exception as e:
        current_app.logger.error(f"Failed to update person {id}: {e}")
        return Response(status=400)


@bp.route("<string:person_id>", methods=["DELETE"])
async def delete_person(user_id: str, person_id: str):
    current_app.logger.info(f"Now deleting person id {person_id} for user {user_id}")

    user_reference: Optional[DocumentReference] = get_user_reference(user_id)
    if user_reference is None:
        return Response(status=404)

    try:
        # save person in memory briefly so we can return it to client after deleting
        person_doc: DocumentReference = user_reference.collection("persons").document(
            person_id
        )
        person_snapshot: DocumentSnapshot = person_doc.get()
        if not person_snapshot.exists:
            return Response(status=404)

        response: Timestamp = person_doc.delete()

        # manually append Document id before returning deleted Person
        person_data: dict = person_snapshot.to_dict()
        person_data["id"] = person_snapshot.id
        return Response(person_data, status=204)

    except Exception as e:
        current_app.logger.info(f"Failed to find person {person_id} to delete: {e}")
        return Response(status=404)
