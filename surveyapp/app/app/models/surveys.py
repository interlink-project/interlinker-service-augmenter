from pydantic import BaseModel, Field, Extra, validator
from typing import Union, Optional
import datetime
from app.config import settings

class AssetCreateUpdateSchema(BaseModel, extra=Extra.allow):
    title: Union[str, object]

class AssetSchema(BaseModel):
    id: str = Field(..., alias='_id')
    created_at: datetime.datetime
    updated_at: Optional[datetime.datetime]

    # extra allowed
    class Config:
        extra = Extra.allow
        allow_population_by_field_name = True

class AssetBasicDataSchema(BaseModel):
    # id: str = Field(alias='_id')
    title: str = Field(alias='name')
    icon: str = "https://cdn.pixabay.com/photo/2017/05/15/23/48/survey-2316468_1280.png"
    createdTime: datetime.datetime = Field(alias='created_at')
    modifiedTime: Optional[datetime.datetime] = Field(alias='updated_at')
   
    class Config:
        allow_population_by_field_name = True
      
    """
    @validator('viewLink', always=True)
    def view_link(cls, name, values):
        asset_id = values["id"]
        return settings.COMPLETE_SERVER_NAME + f"/assets/{asset_id}/view"

    @validator('editLink', always=True)
    def edit_link(cls, name, values):
        asset_id = values["id"]
        return settings.COMPLETE_SERVER_NAME + f"/assets/{asset_id}/edit"
    
    @validator('cloneLink', always=True)
    def clone_link(cls, name, values):
        asset_id = values["id"]
        return settings.COMPLETE_SERVER_NAME + f"/assets/{asset_id}/clone"
    viewLink: Optional[str]
    editLink: Optional[str]
    cloneLink: Optional[str]
    """
    