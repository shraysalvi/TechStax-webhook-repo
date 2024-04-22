from app import mongo
from datetime import datetime, timedelta


DB = mongo.db


def gets():
    """
    Get all the githooks data from the database.

    Returns:
        data (cursor): Cursor object containing all the githooks data.
        error (str): Error message if the event is not found.
    """
    try:
        data = DB.githooks.find({})
        return data
    except Exception as e:
        return {"error": str(e)}


def get(_id: str):
    """
    Get a specific githook event by its ID.

    Args:
        _id (str): ID of the githook event.

    Returns:
        data (dict): Dictionary containing the githook event data.
        error (str): Error message if the event is not found.
    """
    try:
        data = DB.githooks.find_one({"_id": _id})
        if data:
            return data
        else:
            return {"error": "Event not found"}
    except Exception as e:
        return {"error": str(e)}


def insert(event_data: dict):
    """
    Insert a new githook event into the database.

    Args:
        event_data (dict): Dictionary containing the githook event data.

    Returns:
        inserted_id (str): ID of the inserted githook event.
        error (str): Error message if the event is not found.
    """
    try:
        inserted_id = DB.githooks.insert_one(event_data).inserted_id
        return str(inserted_id)
    except Exception as e:
        return {"error": str(e)}


def update(_id: str, event_data: dict):
    """
    Update a githook event in the database.

    Args:
        _id (str): ID of the githook event to be updated.
        event_data (dict): Dictionary containing the updated githook event data.

    Returns:
        message (str): Success message if the event is updated successfully.
        error (str): Error message if the event is not found.
    """
    try:
        result = DB.githooks.update_one({"_id": _id}, {"$set": event_data})
        if result.modified_count > 0:
            return {"message": "Event updated successfully"}
        else:
            return {"error": "Event not found or no changes made"}
    except Exception as e:
        return {"error": str(e)}


def delete(_id: str):
    """
    Delete a githook event from the database.

    Args:
        _id (str): ID of the githook event to be deleted.

    Returns:
        message (str): Success message if the event is deleted successfully.
        error (str): Error message if the event is not found.
    """
    try:
        result = DB.githooks.delete_one({"_id": _id})
        if result.deleted_count > 0:
            return {"message": "Event deleted successfully"}
        else:
            return {"error": "Event not found"}
    except Exception as e:
        return {"error": str(e)}


def delete_old_records():
    """
    Delete githook events that are older than 3 minutes from the database.

    Returns:
        message (str): Success message if the old events are deleted successfully.
        error (str): Error message if there was an error deleting the old events.
    """
    try:
        min3_ago = datetime.now() - timedelta(minutes=3)

        result = DB.githooks.delete_many({"timestamp": {"$lt": min3_ago}})

        if result.deleted_count > 0:
            return {"message": "Old events deleted successfully"}
        else:
            return {"error": "No old events found"}
    except Exception as e:
        return {"error": str(e)}


def last_15min():
    """
    Get the latest 5 githook records from the database.

    Returns:
        data (cursor): Cursor object containing the latest 5 githook records.
    """
    # delete_old_records()

    sec15_ago = datetime.now() - timedelta(seconds=15)
    return DB.githooks.find({"timestamp": {"$gte": sec15_ago}}).sort([("_id", -1)])
