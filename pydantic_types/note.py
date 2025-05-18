from datetime import datetime
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, conint
from tortoise.contrib.pydantic import pydantic_model_creator

from models.notes import Note, NoteStatus
from pydantic_types.medium import MediumSchema

NoteSchema = pydantic_model_creator(Note)

Score = conint(ge=0, le=10)

class NoteGet(BaseModel):
    id: UUID
    user_id: UUID 
    note: str | None
    score: Score
    status: NoteStatus
    medium: MediumSchema
    is_removed: bool
    created_at: datetime
    last_edit_at: datetime | None

class NotesListResponse(BaseModel):
    page: int
    total: int
    has_next: bool
    list: List[NoteSchema]


class NoteCreateRequest(BaseModel):
    note: Optional[str] = ""
    medium_id: UUID


class NoteUpdateRequest(BaseModel):
    status: Optional[NoteStatus] = None
    score: Optional[Score] = None
    note: Optional[str] = None