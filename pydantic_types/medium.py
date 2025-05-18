from datetime import datetime
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator

from models.medium import Medium, MediumType

MediumSchema = pydantic_model_creator(
    Medium,
)

class MediumGet(BaseModel):
    id: UUID
    name: str
    type: MediumType
    image: str | None
    description: str | None
    is_public: bool
    is_removed: bool
    created_at: datetime
    last_edit_at: datetime | None
    creator_id: UUID

class MediumListResponse(BaseModel):
    page: int
    total: int
    has_next: bool
    list: List[MediumSchema]


class MediumCreateRequest(BaseModel):
    name: str
    type: MediumType


class MediumUpdateRequest(BaseModel):
    name: Optional[str] = None
    type: Optional[MediumType] = None
    image: Optional[str] = None
    description: Optional[str] = None
    