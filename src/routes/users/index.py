from quart import Blueprint, current_app, Response, Request, request
from google.cloud.firestore import (
    CollectionReference,
    DocumentReference,
    DocumentSnapshot,
)
from google.cloud.firestore_v1.types import WriteResult
from google.protobuf.timestamp_pb2 import Timestamp

from typing import Optional, Sequence
from datetime import datetime

from ...firestore import User, Firestore

bp = Blueprint("users", __name__)


def get_collection() -> CollectionReference:
    db = Firestore().db
    return db.collection("users")


@bp.route("", methods=["GET"])
async def get_all_users() -> Optional[Sequence[User]]:
    response: Sequence[DocumentReference] = get_collection().list_documents()
    users: list = []
    for user_doc in response:
        user_dict = user_doc.get().to_dict()
        user_dict["id"] = user_doc.id

        users.append(user_dict)

    current_app.logger.info(f"Query returned users: {users}")
    return {"users": users}


@bp.route("", methods=["POST"])
async def create_user() -> Optional[User]:
    request_body = await request.get_json()

    # manually append createdAt attribute
    request_body["createdAt"] = datetime.utcnow()

    # TODO validate shape of request body matches User
    response = get_collection().add(request_body)

    user_reference: DocumentReference = response[1]
    print(f"Created user: {user_reference}")

    # there _should_ be an easier way to retrieve the DocumentReference data and its id
    user = user_reference.get().to_dict()
    user["id"] = user_reference.id
    return user


@bp.route("/<string:id>", methods=["GET"])
async def get_user(id: str) -> Optional[User]:
    current_app.logger.debug(f"Now getting user id {id}")
    try:
        user = get_collection().document(id).get().to_dict()
        current_app.logger.info(f"Found user: {user}")

        if user is None:
            return Response(status=404)
        return user
    except Exception as e:
        current_app.logger.info(f"Failed to get user id {id}: {e}")
        return Response(status=400)


@bp.route("/<string:id>", methods=["PATCH"])
async def patch_user(id: str) -> Optional[User]:
    request_body: dict = await request.get_json()
    current_app.logger.info(f"Now updating user id {id} with body {request_body}")

    # only send fields that we consider updatable
    sanitized_body: dict = {}
    for field in ["firstName", "lastName", "email"]:
        if field in request_body:
            sanitized_body[field] = request_body[field]

    sanitized_body["updatedAt"] = datetime.utcnow()

    try:
        response: WriteResult = get_collection().document(id).update(sanitized_body)

        user_reference: DocumentReference = get_collection().document(id)
        updated_user: dict = user_reference.get().to_dict()
        updated_user["id"] = user_reference.id

        return updated_user

    except Exception as e:
        current_app.logger.error(f"Failed to update user {id}: {e}")
        return Response(status=400)


@bp.route("/<string:id>", methods=["DELETE"])
async def delete_user(id: str) -> Optional[User]:
    current_app.logger.info(f"Now deleting user id {id}")

    try:
        # save user in memory briefly so we can return it to client after deleting
        user: dict = get_collection().document(id).get().to_dict()
        if user is None:
            return Response(status=404)

        response: Timestamp = get_collection().document(id).delete()
        current_app.logger.debug(f"User id {id} deleted at {response}")

        user["id"] = id  # manually append Document id
        return user

    except Exception as e:
        current_app.logger.info(f"Failed to find user id {id} to delete: {e}")
        return Response(status=404)
