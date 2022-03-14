from typing import List

from fastapi import APIRouter, Depends, HTTPException

from app.authentication import get_current_active_user
from app.crud import answers as answers_crud
from app.crud import assets as assets_crud
from app.database import (
    AsyncIOMotorCollection,
    get_collection,
)
from app.models.surveys import AssetCreateUpdateSchema, AssetSchema

customrouter = APIRouter()


@customrouter.get(
    "/assets", response_description="List of survey JSON", response_model=List[AssetSchema]
)
async def list_assets(collection: AsyncIOMotorCollection = Depends(get_collection)):
    return await assets_crud.get_all(collection)


@customrouter.put(
    "/assets/{id}", response_description="Asset JSON"
)
async def update_asset(id: str, asset_in: AssetCreateUpdateSchema, collection: AsyncIOMotorCollection = Depends(get_collection)):
    asset = await assets_crud.get(collection, id)
    if asset:
        return await assets_crud.update(collection, id, asset_in.dict())

    raise HTTPException(status_code=404, detail="Asset {id} not found")


@customrouter.post(
    "/assets/{asset_id}/answers", response_description="List of answers for survey in JSON", response_model=dict
)
async def post_answer(asset_id: str, data: dict, current_user: dict = Depends(get_current_active_user), collection: AsyncIOMotorCollection = Depends(get_collection)):
    return await answers_crud.create(collection=collection, asset_id=asset_id, user_id=current_user["sub"], data=data)


@customrouter.get(
    "/assets/{asset_id}/answers", response_description="List of answers for survey in JSON", response_model=List[dict]
)
async def get_answers(asset_id: str, current_user: dict = Depends(get_current_active_user), collection: AsyncIOMotorCollection = Depends(get_collection)):
    return await answers_crud.get_all(collection, asset_id)


# @customrouter.get(
#     "/example/", response_description="GUI for example survey"
# )
# async def example():
#     survey_id = "548843c87b344cedaa0554276888da6b"
#     html_content = f"""
#     <!DOCTYPE html>
#     <html lang="en">
#
#     <head>
#     <title>Integration example</title>
#     </head>
#
#     <body>
#     Aquí estaría el interlinker y todo su contenido
#     <script src="http://localhost:8921/static/load.js" id="survey-script" data-surveyid="{survey_id}"></script>
#     </body>
#
#     </html>
#     """
#     return HTMLResponse(content=html_content, status_code=200)
