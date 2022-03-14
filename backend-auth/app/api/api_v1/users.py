from typing import Any, List, Optional
import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import AsyncIOMotorCollection, get_collection
from app import deps, crud
from app.model import UserOutSchema

router = APIRouter()

@router.get("/me", response_model=UserOutSchema)
def me(
    current_user: dict = Depends(deps.get_current_active_user),
) -> Any:
    return current_user

@router.get("/{id}", response_model=UserOutSchema)
async def retrieve(
    id: str,
    current_user: dict = Depends(deps.get_current_user),
    collection: AsyncIOMotorCollection = Depends(get_collection)
) -> Any:
    user = await crud.get(collection, id)
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id '{id}' not found")
    return user