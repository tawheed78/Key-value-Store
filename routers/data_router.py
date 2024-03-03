"""Configuration module for routes"""

from fastapi import APIRouter, HTTPException
from models.database_model import KeyValueDb
from db_config import client, db
from redis_config import huey


router = APIRouter()

collection = db["logs_data"]


@huey.task()
def store_data_in_db(data: KeyValueDb):
    """Stores data in the database.

    Args:
        data (KeyValueDb): The data to be added to the database.

    Raises:
        HTTPException: If an error occurs while adding the data.

    """
    try:
        document = {"_id": data.key, "value": data.value}
        collection.insert_one(document)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


async def get_data_from_db(key: str) -> dict:
    """Gets data from the database.

    Args:
        key (str): The key to the data value.

    Raises:
        HTTPException: If an error occurs while getting the data.

    """
    try:
        if not key:
            raise HTTPException(status_code=400, detail="Key is required")
        document = await collection.find_one({"_id": key})
        if document is None:
            raise HTTPException(status_code=404, detail="Data not found")
        return document
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@huey.task()
def update_data_in_db(key: str, data: KeyValueDb):
    """Updates data in the database.

    Args:
        key (str), data (KeyValueDb): The key of the data to be updated along with the data.

    Raises:
        HTTPException: If an error occurs while updating the data.

    """
    try:
        document_to_update = {"_id": key}
        data_to_be_updated = {"$set": {"value": data.value}}
        collection.update_one(
            document_to_update, data_to_be_updated, upsert=True
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@huey.task()
def delete_data_from_db(key: str):
    """Deletes data from the database.

    Args:
        key (str): The key to the data value.

    Raises:
        HTTPException: If an error occurs while deleting the data.

    """
    try:
        document_to_delete = {"_id": key}
        collection.delete_one(document_to_delete)
        return {"message": "Data deleted succesfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/post-data/")
async def post_data(data: KeyValueDb):
    """Post data to the database.

    Args:
        data (KeyValueDb): The data to be posted.

    Returns:
        dict: A dictionary containing a success message if the data is uploaded successfully.

    Raises:
        HTTPException: If an error occurs while posting the data.

    """
    try:
        if client is None:
            raise HTTPException(status_code=500, detail="No connection to the database")
        if not data.key or not data.value:
            raise HTTPException(status_code=400, detail="Key and value is required")

        existing_document = await collection.find_one({"_id": data.key})
        if existing_document:
            raise HTTPException(status_code=400, detail="Key already exists")
        store_data_in_db(data)
        return {"message": "Data uploaded succesfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/get-data/")
async def get_data(key: str):
    """Retrieve data from the database based on the provided key.

    Args:
        key (str): The key used to retrieve data from the database.

    Returns:
        dict: A dictionary containing the retrieved data.

    Raises:
        HTTPException: No connection to the database or an error occurs during data retrieval.

    """
    if client is None:
        raise HTTPException(status_code=500, detail="No connection to the database")

    result = await get_data_from_db(key)
    return result


@router.put("/update-data/")
async def update_data(key: str, data: KeyValueDb):
    """Update data in the database using the provided key referring to the data.

    Args:
        key (str): The key used to identify the data to be updated.
        data (KeyValueDb): The data to be updated.

    Returns:
        dict: A dictionary containing a success message on successful operation.

    Raises:
        HTTPException: No connection to the database, missing key, or error in the update process.
    """
    try:
        if client is None:
            raise HTTPException(status_code=500, detail="No connection to the database")
        if not key or not data:
            raise HTTPException(status_code=400, detail="Key is required")
        update_data_in_db(key, data)
        return {"message": "Data updated succesfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.delete("/delete-data/")
async def delete_data(key: str):
    """Delete data from the database based with the provided key.

    Args:
        key (str): The key used to identify the data to be deleted.

    Returns:
        dict: A dictionary containing a success message if the deletion is successful.

    Raises:
        HTTPException: No connection to the database, missing key, data doesn't exist, 
        or error in deletion process.
    """
    try:
        if client is None:
            raise HTTPException(status_code=500, detail="No connection to the database")
        if not key:
            raise HTTPException(status_code=400, detail="Key is required")

        existing_document = await collection.find_one({"_id": key})
        if not existing_document:
            raise HTTPException(status_code=400, detail="Data does not exists")

        delete_data_from_db(key)
        return {"message": "Data deleted succesfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
