from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, Query

from models.user import User
from services.medium import medium_service
from pydantic_types.medium import MediumCreateRequest, MediumGet, MediumListResponse, MediumSchema, MediumUpdateRequest
from pydantic_types.shared import MessageResponse
from utils.auth import get_current_user


medium_router = APIRouter(prefix='/medium')


@medium_router.get(
    '/list',
    tags=["medium"],
    description="Method that returns list of mediums",
    response_model=MediumListResponse,
)
async def get_medium_search(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    search_phrase: Optional[str] = Query(None),
    user: User = Depends(get_current_user)
):
    return await medium_service.get_list(page=page, limit=limit, search_phrase=search_phrase)


@medium_router.post(
    '/create',
    tags=["medium"],
    description="Method that creates new medium - minimal",
    response_model=MessageResponse,
)
async def create_medium(
    new_medium: MediumCreateRequest,
    user: User = Depends(get_current_user)
):
    return await medium_service.crate(new_medium.name, new_medium.type, user.id, user.email)


@medium_router.get(
    '/{medium_id}',
    tags=["medium"],
    description="Method that returns medium by id",
    response_model=MediumGet,
)
async def get_medium(
    medium_id: UUID,
    user: User = Depends(get_current_user)
):
    return await medium_service.get(medium_id=medium_id)


@medium_router.patch(
    '/{medium_id}',
    tags=["medium"],
    description="Method that update medium",
    response_model=MessageResponse,
)
async def update_medium(
    medium_id: UUID,
    data: MediumUpdateRequest,
    user: User = Depends(get_current_user)
):
    return await medium_service.update(medium_id, data, user)


@medium_router.delete(
    '/{medium_id}',
    tags=["medium"],
    description="Method that softly deletes medium",
    response_model=MessageResponse,
)
async def delete_medium(
    medium_id: UUID,
    user: User = Depends(get_current_user)
):
    return await medium_service.soft_delete(medium_id, user)
