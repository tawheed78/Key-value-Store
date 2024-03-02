from fastapi import APIRouter, HTTPException
from models.database_model import Key_value_Db
from config import client, db
from pymongo.errors import DuplicateKeyError

router = APIRouter()

collection = db['logs_data']

async def store_data_in_db(data: Key_value_Db):
    try:
        if not data.key:
            raise HTTPException(status_code=400, detail="Key is required")
        document = {
            "_id" : data.key,
            "value" : data.value
        }
        result = await collection.insert_one(document)
        return {"message" : "Data uploaded succesfully"}
    except DuplicateKeyError:
        raise HTTPException(status_code=400, detail="Key already exists")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def get_data_from_db(key:str) -> dict:
    try:
        if not key:
            raise HTTPException(status_code=400, detail="Key is required")
        document = await collection.find_one({"_id": key})
        if document is None:
            raise HTTPException(status_code=404, detail="Data not found")
        return document
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

async def update_data_in_db(key : str, data : Key_value_Db):
    try:
        if not key:
            raise HTTPException(status_code=400, detail="Key is required")
        document_to_update = {"_id" : key}
        data_to_be_updated = {"$set" : {"value" : data.value}}
        result = await collection.update_one(document_to_update, data_to_be_updated, upsert=True)
        return {"message" : "Data updated succesfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
async def delete_data_from_db(key : str):
    try:
        if not key:
            raise HTTPException(status_code=400, detail="Key is required")
        document_to_delete = {"_id" : key}
        result = await collection.delete_one(document_to_delete)
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Data not found")
        return {"message" : "Data deleted succesfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    


@router.post('/post-data/')
async def post_data(data : Key_value_Db):
    if client is None:
        raise HTTPException(status_code=500, detail="No connection to the database")
    
    result = await store_data_in_db(data)
    return result

@router.get('/get-data/')
async def get_data(key : str):
    if client is None:
        raise HTTPException(status_code=500, detail="No connection to the database")
    
    result = await get_data_from_db(key)
    return result

@router.put('/update-data/')
async def update_data(key : str, data : Key_value_Db):
    if client is None:
        raise HTTPException(status_code=500, detail="No connection to the database")
    
    result = await update_data_in_db(key, data)
    return result

@router.delete('/delete-data/')
async def delete_data(key : str):
    if client is None:
        raise HTTPException(status_code=500, detail="No connection to the database")
    
    result = await delete_data_from_db(key)
    return result