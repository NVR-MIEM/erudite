from fastapi import APIRouter
import logging

from ..database.models import (
    ErrorResponseModel,
    ResponseModel,
    Response,
)
from ..database.rooms import get_all, get, add, add_empty, get_by_name, remove, patch_additional, patch_all, Room
from ..database.utils import mongo_to_dict, check_ObjectId
from ..database.equipment import sort

router = APIRouter()

logger = logging.getLogger("erudite")


@router.get(
    "/rooms",
    tags=["rooms"],
    summary="Get all rooms",
    description="Get a list of all rooms in the database",
    response_model=Response,
)
async def list_rooms():
    return ResponseModel(200, await get_all(), "Rooms returned successfully")


@router.get(
    "/rooms/{room_id}",
    tags=["rooms"],
    summary="Get a room",
    description="Get a room specified by it's ObjectId",
    response_model=Response,
)
async def find_room(room_id: str):
    # Check if ObjectId is in the right format
    id = check_ObjectId(room_id)

    if id:
        # Check if room with specified ObjectId is in the database
        room = await get(id)
        if room:
            logger.info(f"Room {room_id}: {room}")
            return ResponseModel(200, room, "Room returned successfully")
        else:
            message = "This room is not found"
            logger.info(message)
            return ErrorResponseModel(404, message)
    else:
        message = "ObjectId is written in the wrong format"
        return ErrorResponseModel(400, message)


@router.post(
    "/rooms",
    tags=["rooms"],
    summary="Create room",
    description="Create a room specified by it's ObjectId",
    response_model=Response,
)
async def create_room(room: Room):
    # Check if room with specified ObjectId is in the database
    if await get_by_name(room.name):
        message = f"Room with name: '{room.name}'  -  already exists in the database"
        logger.info(message)
        return ErrorResponseModel(403, message)
    else:
        new_room = await add(room)
        logger.info(f"Room: {room.name}  -  added to the database")
        return ResponseModel(201, new_room, "Room added successfully")


@router.delete(
    "/rooms/{room_id}",
    tags=["rooms"],
    summary="Delete room",
    description="Delete room specified by it's ObjectId",
    response_model=Response,
)
async def delete_room(room_id: str):
    # Check if ObjectId is in the right format
    id = check_ObjectId(room_id)

    if id:
        if await get(id):
            await remove(id)
            message = f"Room: {room_id}  -  deleted from the database"
            logger.info(message)
            return ResponseModel(200, message, "Room deleted successfully")
        # Check if room with specified ObjectId is in the database
        else:
            message = f"Room: {room_id}  -  not found in the database"
            logger.info(message)
            return ErrorResponseModel(404, message)
    else:
        message = "ObjectId is written in the wrong format"
        return ErrorResponseModel(400, message)


@router.patch(
    "/rooms/{room_id}",
    tags=["rooms"],
    summary="Patch room",
    description="Updates additional atributes of room specified by it's ObjectId",
    response_model=Response,
)
async def patch_room(room_id: str, new_values: dict):
    # Check if ObjectId is in the right format
    id = check_ObjectId(room_id)

    if id:
        if await get(id):
            await patch_additional(id, new_values)
            message = f"Room: {room_id}  -  pached"
            logger.info(message)
            return ResponseModel(200, message, "Room patched successfully")
        # Check if room with specified ObjectId is in the database
        else:
            message = f"Room: {room_id}  -  not found in the database"
            logger.info(message)
            return ErrorResponseModel(404, message)
    else:
        message = "ObjectId is written in the wrong format"
        return ErrorResponseModel(400, message)


@router.put(
    "/rooms/{room_id}",
    tags=["rooms"],
    summary="Updates room",
    description="Deletes old atributes of room specified by it's ObjectId and puts in new ones",
    response_model=Response,
)
async def update_room(room_id: str, new_values: Room):
    # Check if ObjectId is in the right format
    id = check_ObjectId(room_id)

    if id:
        if await get(id):
            await remove(id)
            await add_empty(id)
            await patch_all(id, new_values)
            message = f"Room: {room_id}  -  updated"
            logger.info(message)
            return ResponseModel(200, message, "Room updated successfully")
        # Check if room with specified ObjectId is in the database
        else:
            message = f"Room: {room_id}  -  not found in the database"
            logger.info(message)
            return ErrorResponseModel(404, message)
    else:
        message = "ObjectId is written in the wrong format"
        return ErrorResponseModel(400, message)


@router.get(
    "/rooms/{room_id}/equipment",
    tags=["rooms"],
    summary="Get equipment from the room",
    description="Get a list of equipment from the room specified by it's ObjectId",
    response_model=Response,
)
async def list_room_equipments(room_id: str):
    # Check if ObjectId is in the right format
    id = check_ObjectId(room_id)

    if id:
        room = await get(id)
        if room:
            data = await sort(id)
            print(data)
            return ResponseModel(200, data, "Room updated successfully")
        # Check if equipment with specified room_id is in the database
        else:
            message = "This room is not found"
            logger.info(message)
            return ErrorResponseModel(404, message)
    else:
        message = "ObjectId is written in the wrong format"
        return ErrorResponseModel(400, message)
