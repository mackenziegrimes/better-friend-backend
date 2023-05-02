from quart import Blueprint, current_app, Request, Response, request
from datetime import datetime
from typing import Optional, Sequence

from google.cloud.firestore import (
    DocumentReference,
    DocumentSnapshot,
    CollectionReference,
)
from google.cloud.firestore_v1.types import WriteResult

from ...firestore import Connection, Person, get_collection

bp = Blueprint("connections", __name__)


def get_person_reference(user_id: str, person_id: str) -> Optional[DocumentReference]:
    person_reference: DocumentReference = (
        get_collection().document(user_id).collection("persons").document(person_id)
    )
    return person_reference if person_reference.get().exists else None


@bp.route("", methods=["GET"])
async def get_all_connections(user_id: str, person_id: str):
    person_reference: Optional[DocumentReference] = get_person_reference(
        user_id, person_id
    )
    if person_reference is None:
        return Response(status=404)

    try:
        connection_collections: Sequence[
            CollectionReference
        ] = person_reference.collections()

        # loop through DocumentReference list and build Connection model object
        connections: Sequence[dict] = []
        for collection in connection_collections:
            for doc in collection.stream():
                connection_data = doc.to_dict()
                connection_data["id"] = doc.id
                connections.append(connection_data)

        return {"connections": connections}
    except Exception as e:
        current_app.logger.error(
            f"Failed to get connections for person {person_id}, user {user_id}: {e}"
        )
        return Response("Internal server error", status=500)


@bp.route("", methods=["POST"])
async def create_connect(user_id: str, person_id: str) -> Optional[Connection]:
    request_data = await request.get_json()
    current_app.logger.info(
        f"Creating connection for person {person_id} with body: {request_data}"
    )

    # TODO validate request body
    person_reference: Optional[DocumentReference] = get_person_reference(
        user_id, person_id
    )
    if person_reference is None:
        return Response(status=404)

    try:
        # create new connections document in connections subcollection under this person
        connections_reference: CollectionReference = person_reference.collection(
            "connections"
        )
        connection_doc: DocumentReference = connections_reference.document()

        # set createdAt of now if it wasn't passed by the client
        if "createdAt" not in request_data:
            request_data["createdAt"] = datetime.utcnow()

        connection_doc.create(request_data)

        # append the id to the rest of the data before returning
        connection_data: dict = connection_doc.get().to_dict()
        connection_data["id"] = connection_doc.id

        current_app.logger.info(f"Created connection: {connection_data}")
        return Response(connection_data, status=201)
    except Exception as e:
        current_app.logger.error(
            f"Failed to create connection for person {person_id} and user {user_id}: {e}"
        )
        return Response("Internal server error", status=500)


@bp.route("<string:connection_id>", methods=["GET"])
async def get_connection(
    user_id: str, person_id: str, connection_id: str
) -> Optional[Connection]:
    current_app.logger.info(
        f"Now getting connection_id {connection_id} under person_id {person_id}"
    )

    person_reference: Optional[DocumentReference] = get_person_reference(
        user_id, person_id
    )
    if person_reference is None:
        return Response(status=404)

    connection_snapshot: DocumentSnapshot = (
        person_reference.collection("connections").document(connection_id).get()
    )
    if not connection_snapshot.exists:
        return Response(status=404)

    # manually append data to the constructed Connection object
    data = connection_snapshot.to_dict()
    data["id"] = connection_snapshot.id
    return data


@bp.route("<string:connection_id>", methods=["PATCH"])
async def patch_connection(
    user_id: str, person_id: str, connection_id: str
) -> Optional[Connection]:
    request_body: dict = await request.get_json()
    current_app.logger.info(
        f"Now updating connection_id {connection_id} with body {request_body}"
    )

    # get base User document which has persons nested collection, if it exists
    person_reference: Optional[DocumentReference] = get_person_reference(
        user_id, person_id
    )
    if person_reference is None:
        return Response(status=404)

    # only send fields that we consider updatable
    sanitized_body: dict = {}
    for field in ["createdAt", "notes"]:
        if field in request_body:
            sanitized_body[field] = request_body[field]

    try:
        connection_ref: DocumentReference = person_reference.collection(
            "connections"
        ).document(connection_id)
        if not connection_ref.get().exists:
            return Response(status=404)

        connection_ref.update(sanitized_body)

        # manually append data to the constructed Connection object
        data = connection_ref.get().to_dict()
        data["id"] = connection_ref.id
        return data
    except Exception as e:
        current_app.logger.info(f"Failed to update connection {id}: {e}")
        return Response(status=400)


@bp.route("<string:connection_id>", methods=["DELETE"])
async def delete_connection(
    user_id: str, person_id: str, connection_id: str
) -> Optional[Connection]:
    current_app.logger.info(
        f"Now deleting connection_id {connection_id} under person_id {person_id}"
    )

    person_reference: Optional[DocumentReference] = get_person_reference(
        user_id, person_id
    )
    if person_reference is None:
        return Response(status=404)

    try:
        # save connection in memory so we can return it to client after deleting
        connection_doc: DocumentReference = person_reference.collection(
            "connections"
        ).document(connection_id)
        connection_snapshot: DocumentSnapshot = connection_doc.get()
        if not connection_doc.get().exists:
            return Response(status=404)

        response: Timestamp = connection_doc.delete()

        # manually append id before returning the deleted Connection object
        data: dict = connection_snapshot.to_dict()
        data["id"] = connection_snapshot.id
        return Response(data, status=204)
    except Exception as e:
        current_app.logger.info(
            f"Failed to find connection {connection_id} to delete: {e}"
        )
        return Response(status=404)
