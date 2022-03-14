import json

from fastapi import APIRouter, Depends, FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse

from app.config import settings
from app.crud import assets as crud
from app.database import AsyncIOMotorCollection, get_collection
from app.models.surveys import AssetBasicDataSchema, AssetCreateUpdateSchema, AssetSchema
from app.api.v1.common import templates, domainfo
from app.authentication import get_current_active_user

integrablerouter = APIRouter()

@integrablerouter.post("/assets", response_description="Asset JSON", response_model=AssetSchema, status_code=201)
async def create_asset(survey: AssetCreateUpdateSchema, collection: AsyncIOMotorCollection = Depends(get_collection)):
    return await crud.create(collection, survey)


@integrablerouter.get(
    "/assets/instantiate", response_description="GUI for asset creation"
)
async def instantiate_asset(request: Request):
    return templates.TemplateResponse("instantiator.html", {"request": request, "BASE_PATH": settings.BASE_PATH, "DOMAIN_INFO": json.dumps(domainfo)})


@integrablerouter.get(
    "/assets/{id}", response_description="Asset JSON", response_model=AssetBasicDataSchema
)
async def asset_data(id: str, collection: AsyncIOMotorCollection = Depends(get_collection)):
    if (asset := await crud.get(collection, id)) is not None:
        return asset

    raise HTTPException(status_code=404, detail=f"Asset {id} not found")


@integrablerouter.delete("/assets/{id}", response_description="No content")
async def delete_asset(id: str, collection: AsyncIOMotorCollection = Depends(get_collection)):
    if crud.get(collection, id) is not None:
        delete_result = await crud.delete(collection, id)
        if delete_result.deleted_count == 1:
            return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Asset with id {id} not found")


@integrablerouter.get(
    "/assets/{id}/view", response_description="GUI for viewing survey"
)
async def asset_viewer(id: str, request: Request, current_user: dict = Depends(get_current_active_user), collection: AsyncIOMotorCollection = Depends(get_collection)):
    survey = await crud.get(collection, id)
    if survey is not None:
        response = templates.TemplateResponse("surveyviewer.html", {
                                              "request": request, "BASE_PATH": settings.BASE_PATH, "DOMAIN_INFO": json.dumps(domainfo), "DATA": json.dumps(survey, indent=4, sort_keys=True, default=str), "title": survey["title"]})
        return response

    raise HTTPException(status_code=404, detail=f"Asset {id} not found")


@integrablerouter.get(
    "/assets/{id}/edit", response_description="GUI for editing specific survey"
)
async def asset_editor(id: str, request: Request, collection: AsyncIOMotorCollection = Depends(get_collection)):
    survey = await crud.get(collection, id)
    if survey is not None:
        response = templates.TemplateResponse("surveybuilder.html", {
                                              "request": request,  "BASE_PATH": settings.BASE_PATH, "DOMAIN_INFO": json.dumps(domainfo), "DATA": json.dumps(survey, indent=4, sort_keys=True, default=str)})
        return response

    raise HTTPException(status_code=404, detail=f"Asset {id} not found")


@integrablerouter.post(
    "/assets/{id}/clone", response_description="Asset JSON", status_code=201, response_model=AssetBasicDataSchema
)
async def clone_asset(id: str, collection: AsyncIOMotorCollection = Depends(get_collection)):
    if (survey := await crud.get(collection, id)) is not None:
        return await crud.create(collection, AssetCreateUpdateSchema(**survey))

    raise HTTPException(status_code=404, detail="Asset {id} not found")
