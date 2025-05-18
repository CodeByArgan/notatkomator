from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, Query

from models.user import User
from pydantic_types.note import NoteCreateRequest, NoteGet, NoteUpdateRequest, NotesListResponse
from services.notes import notes_service
from pydantic_types.shared import MessageResponse
from utils.auth import get_current_user


notes_router = APIRouter(prefix='/notes')


@notes_router.get(
    '/list',
    tags=["notes"],
    description="Method that returns list of notes",
    response_model=NotesListResponse,
)
async def get_notes_search(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    search_phrase: Optional[str] = Query(""),
    user: User = Depends(get_current_user)
):
    return await notes_service.get_list(page=page, limit=limit, search_phrase=search_phrase, user=user)


@notes_router.post(
    '/create',
    tags=["notes"],
    description="Method that creates new note",
    response_model=MessageResponse,
)
async def create_note(
    new_note: NoteCreateRequest,
    user: User = Depends(get_current_user)
):
    return await notes_service.crate(new_note.note, new_note.medium_id, user)


@notes_router.get(
    '/{note_id}',
    tags=["notes"],
    description="Method that returns note by id",
    response_model=NoteGet,
)
async def get_medium(
    note_id: UUID,
    user: User = Depends(get_current_user)
):
    return await notes_service.get(note_id=note_id, user=user)


@notes_router.patch(
    '/{note_id}',
    tags=["notes"],
    description="Method that update note",
    response_model=MessageResponse,
)
async def update_medium(
    note_id: UUID,
    data: NoteUpdateRequest,
    user: User = Depends(get_current_user)
):
    return await notes_service.update(note_id, data, user)


@notes_router.delete(
    '/{note_id}',
    tags=["notes"],
    description="Method that softly deletes note",
    response_model=MessageResponse,
)
async def delete_note(
    note_id: UUID,
    user: User = Depends(get_current_user)
):
    return await notes_service.soft_delete(note_id, user)
