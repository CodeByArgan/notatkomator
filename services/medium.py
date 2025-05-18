from datetime import datetime, timezone
from uuid import UUID

from fastapi import HTTPException
from models.user import User
from services.audit_log import audit_log_service
from models.medium import Medium, MediumType
from pydantic_types.medium import MediumListResponse, MediumUpdateRequest
from utils.logger import logger

class MediumService():

    async def get(self, medium_id: UUID):
        medium = await Medium.get_or_none(id=medium_id, is_removed=False)
        
        if not medium:
            raise HTTPException(status_code=404, detail="Medium not found")
        
        return medium
     

    async def update(self, medium_id: UUID, data: MediumUpdateRequest, user: User):
        medium = await self.get(medium_id)

        update_data = data.model_dump(exclude_unset=True)
        logger.info(update_data)
        for field, value in update_data.items():
            setattr(medium, field, value)
        
        medium.last_edit_at = datetime.now(timezone.utc)

        await medium.save()
        
        await audit_log_service.create_new(user.email, f"User {user.email} edited medium {medium.id}:{medium.name}")

        return {"message": "ok"}
    
 
    async def soft_delete(self, medium_id: UUID, user: User):
        medium = await self.get(medium_id)

        if  medium.creator_id == user.id or user.role == "admin":
            medium.is_removed = True
            await medium.save()
            
            await audit_log_service.create_new(user.email, f"User {user.email} deleted medium {medium.id}:{medium.name}")
            return {"message": "ok"}
        else:
            raise HTTPException(status_code=403, detail="This user is not an owner of this medium")
   

    async def crate(self, name: str, type: MediumType, user_id: UUID, username: str):
        logger.info(
            "User %s is trying to add new medium named %s typed %s", username, name, type
        )
        await audit_log_service.create_new(username, f"Attempt to create new medium named: {name} type: {type}")
        logger.info(f"User id : {user_id}")
        
        user = await User.get(id=str(user_id))
        await Medium.create(
            name=name, 
            type=type,
            creator=user
        )
        await audit_log_service.create_new(username, f"Successfully created new medium named: {name} type: {type}")
    
    
        return {"message": "ok"}

    async def get_list(self, page: int, limit: int, search_phrase: str) -> MediumListResponse:
        offset = (page - 1) * limit
        logger.info(
            "Get list of medium page: %s limit: %s offset: %s", page, limit, offset, search_phrase)
        if search_phrase:
            mediums = await Medium.filter(name__icontains=search_phrase).all().order_by("-name").offset(offset).limit(limit)
            total = await Medium.filter(name__icontains=search_phrase).all().count()
        else:
            mediums = await Medium.all().order_by("-name").offset(offset).limit(limit)
            total = await Medium.all().count()
        
        has_next = (page * limit) < total

        return {
            "page": page,
            "total": total,
            "list": mediums,
            "has_next": has_next
        }


medium_service = MediumService()