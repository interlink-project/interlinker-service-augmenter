from fastapi.encoders import jsonable_encoder
import uuid 
import datetime
from app.crud import assets as assets_crud

TYPE = "answer"

async def get(collection, id: str):
    return await collection.find_one({"_id": id, "type": TYPE})

async def get_all(collection, survey_id):
    return await collection.find({"asset_id": survey_id, "type": TYPE}).to_list(1000)

async def create(collection, asset_id: str, user_id: str, data: dict):
    obj = {"data": data}
    if assets_crud.get(collection, asset_id):
        obj["type"] = TYPE
        obj["_id"] = uuid.uuid4().hex
        obj["created_at"] = datetime.datetime.now()
        obj["user_id"] = user_id
        obj["asset_id"] = asset_id
        obj = jsonable_encoder(obj)
        db_answer = await collection.insert_one(obj)
        return await get(collection, db_answer.inserted_id)
    else:
        raise Exception("Asset does not exist")

async def update(collection, id: str, data):
    data["updated_at"] = datetime.datetime.now()
    await collection.update_one( { "_id": id, "type": TYPE }, { "$set": data })
    return await get(collection,id)
    
async def delete(collection, id: str):
    return await collection.delete_one({ "_id": id, "type": TYPE })