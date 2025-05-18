from fastapi import APIRouter, Depends, Query

from models.user import User
from pydantic_types.audit_log import AuditLogListResponse
from services.audit_log import audit_log_service
from utils.auth import get_current_user


audit_log_router = APIRouter(prefix="/audit-log")


@audit_log_router.get(
    '/list',
    tags=["audit log"],
    description="Method that returns paginated list of audit logs",
    response_model=AuditLogListResponse,
)
async def get_audit_log_list(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    user: User = Depends(get_current_user)
) -> AuditLogListResponse:
    return await audit_log_service.get_list(page, limit)


@audit_log_router.post(
    '/test-create',
    tags=["audit log"],
    description="Method that created testing audit log",
)
async def create_testing_audit_log_message(user: User = Depends(get_current_user)):
    await audit_log_service.create_new(username="SYSTEM", details="TEST_MESSAGE")
    return {"message": "ok"}
