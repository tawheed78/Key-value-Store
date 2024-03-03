import json
from fastapi import APIRouter, HTTPException
from models.database_model import KeyValueDb
from db_config import client, db
from redis_config import huey


router = APIRouter()

collection = db["logs_data"]


@huey.task()
def store_data_in_db(data: KeyValueDb):
    try:
        document = {"_id": data.key, "value": data.value}
        result = collection.insert_one(document)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def get_data_from_db(key: str) -> dict:
    try:
        if not key:
            raise HTTPException(status_code=400, detail="Key is required")
        document = await collection.find_one({"_id": key})
        if document is None:
            raise HTTPException(status_code=404, detail="Data not found")
        return document
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@huey.task()
def update_data_in_db(key: str, data: KeyValueDb):
    try:
        document_to_update = {"_id": key}
        data_to_be_updated = {"$set": {"value": data.value}}
        result = collection.update_one(
            document_to_update, data_to_be_updated, upsert=True
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@huey.task()
def delete_data_from_db(key: str):
    try:
        document_to_delete = {"_id": key}
        result = collection.delete_one(document_to_delete)
        return {"message": "Data deleted succesfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/post-data/")
async def post_data(data: KeyValueDb):
    try:
        if client is None:
            raise HTTPException(status_code=500, detail="No connection to the database")
        if not data.key or not data.value:
            raise HTTPException(status_code=400, detail="Key and value is required")

        existing_document = await collection.find_one({"_id": data.key})
        if existing_document:
            raise HTTPException(status_code=400, detail="Key already exists")
        else:
            store_data_in_db(data)
            return {"message": "Data uploaded succesfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/get-data/")
async def get_data(key: str):
    if client is None:
        raise HTTPException(status_code=500, detail="No connection to the database")

    result = await get_data_from_db(key)
    return result


@router.put("/update-data/")
async def update_data(key: str, data: KeyValueDb):
    try:
        if client is None:
            raise HTTPException(status_code=500, detail="No connection to the database")
        if not key or not data:
            raise HTTPException(status_code=400, detail="Key is required")
        update_data_in_db(key, data)
        return {"message": "Data updated succesfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/delete-data/")
async def delete_data(key: str):
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
        raise HTTPException(status_code=500, detail=str(e))
