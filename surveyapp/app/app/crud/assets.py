from fastapi.encoders import jsonable_encoder
from app.models.surveys import AssetCreateUpdateSchema
import uuid 
import datetime

TYPE = "asset"


async def get(collection, id: str):
    return await collection.find_one({"_id": id, "type": TYPE})

async def get_all(collection):
    return await collection.find().to_list(1000)

async def create(collection, asset: AssetCreateUpdateSchema):
    asset = asset.__dict__
    asset["type"] = TYPE
    asset["_id"] = uuid.uuid4().hex
    asset["created_at"] = datetime.datetime.now()
    asset = jsonable_encoder(asset)
    db_survey = await collection.insert_one(asset)
    return await get(collection, db_survey.inserted_id)

async def update(collection, id: str, data):
    data["updated_at"] = datetime.datetime.now()
    await collection.update_one( { "_id": id, "type": TYPE }, { "$set": data })
    return await get(collection,id)
    
async def delete(collection, id: str):
    return await collection.delete_one({"_id": id, "type": TYPE})