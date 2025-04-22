from typing import List, Type
from pydantic import BaseModel
from tortoise import Tortoise
from tortoise.contrib.pydantic import pydantic_model_creator
from models.audit_log import AuditLog

AuditLogSchema = pydantic_model_creator(AuditLog)


class AuditLogListResponse(BaseModel):
    page: int
    total: int
    has_next: bool
    list: List[AuditLogSchema]
