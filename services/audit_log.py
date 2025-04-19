
from utils.logger import logger
from models.audit_log import AuditLog
from pydantic_types.audit_log import AuditLogListResponse


class AuditLogService():

    async def get_list(self, page: int, limit) -> AuditLogListResponse:
        offset = (page - 1) * limit
        logger.info(
            "Get list of audit logs page: %s limit: %s offset: %s", page, limit, offset)
        audit_logs = await AuditLog.all().order_by("-created_at").offset(offset).limit(limit)
        total = await AuditLog.all().count()
        has_next = (page * limit) < total

        return {
            "page": page,
            "total": total,
            "audit_logs": audit_logs,
            "has_next": has_next
        }

    async def create_new(self, username: str, details: str):
        logger.info(
            "User %s created new audit details %s", username, details)
        return await AuditLog.create(username=username, details=details)


audit_log_service = AuditLogService()
