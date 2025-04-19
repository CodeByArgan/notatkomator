from fastapi import APIRouter, Query

from pydantic_types.audit_log import AuditLogListResponse
from services.audit_log import audit_log_service


audit_log_router = APIRouter()


@audit_log_router.get(
    '/audit-log/list',
    tags=["audit log"],
    description="Method that returns paginated list of audit logs",
    response_model=AuditLogListResponse,
)
async def get_audit_log_list(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100)
) -> AuditLogListResponse:
    return await audit_log_service.get_list(page, limit)


@audit_log_router.post(
    '/audit-log/test-create',
    tags=["audit log"],
    description="Method that created testing audit log",
)
async def create_testing_audit_log_message():
    await audit_log_service.create_new(username="SYSTEM", details="TEST_MESSAGE")
    return {"message": "ok"}
