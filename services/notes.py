from datetime import datetime, timezone
from uuid import UUID

from fastapi import HTTPException
from models.notes import Note
from models.user import User
from services.audit_log import audit_log_service
from services.medium import medium_service
from pydantic_types.medium import MediumListResponse, MediumUpdateRequest
from utils.logger import logger

class NotesService():

    async def get(self, note_id: UUID, user: User):
        note = await Note.filter(id=note_id, is_removed=False, user_id=user.id).select_related('medium').get_or_none()
        
        if not note:
            raise HTTPException(status_code=404, detail="Note not found")
        
        return note
     

    async def update(self, note_id: UUID, data: MediumUpdateRequest, user: User):
        note = await self.get(note_id, user)

        update_data = data.model_dump(exclude_unset=True)
        logger.info(update_data)
        for field, value in update_data.items():
            setattr(note, field, value)
        
        note.last_edit_at = datetime.now(timezone.utc)

        await note.save()
        await audit_log_service.create_new(user.email, f"User {user.email} edited note {note.id}")

        return {"message": "ok"}
    
 
    async def soft_delete(self, note_id: UUID, user: User):
        note = await self.get(note_id, user)

        if  note.user_id == user.id or user.role == "admin":
            note.is_removed = True
            await note.save()
            
            await audit_log_service.create_new(user.email, f"User {user.email} deleted note {note.id}")
            return {"message": "ok"}
        else:
            raise HTTPException(status_code=403, detail="This user is not an owner of this note")
   

    async def crate(self, note: str, medium_id: UUID, user: User):
        logger.info(
            "User %s is trying to add new note using medium id: %s", user.email, medium_id
        )
        await audit_log_service.create_new(user.email, f"Attempt to create new note using medium id: {medium_id}")

        is_medium_used = await Note.get_or_none(medium_id=medium_id, is_removed=False)
        if is_medium_used is not None:
            await audit_log_service.create_new(user.email, f"User already has medium on his list with this id {medium_id}")
            raise HTTPException(status_code=409, detail="This medium us already on list")

        medium = await medium_service.get(medium_id)

        await Note.create(
            note=note, 
            medium=medium,
            user=user
        )
        await audit_log_service.create_new(user.email, f"Successfully created new note using medium id: {medium_id}")
    
        
        return {"message": "ok"}

    async def get_list(self, page: int, limit: int, search_phrase: str, user: User) -> MediumListResponse:
        offset = (page - 1) * limit
        logger.info(
            "Get list of notes page: %s limit: %s offset: %s", page, limit, offset, search_phrase)
        notes = await Note.filter(note__icontains=search_phrase, user_id=user.id).all().order_by("-created_at").offset(offset).limit(limit)
        total = await Note.filter(note__icontains=search_phrase, user_id=user.id).all().count()
        
        has_next = (page * limit) < total

        return {
            "page": page,
            "total": total,
            "list": notes,
            "has_next": has_next
        }


notes_service = NotesService()