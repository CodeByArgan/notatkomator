from tortoise.models import Model
from tortoise.fields import TextField, UUIDField, DatetimeField


class AuditLog(Model):
    id = UUIDField(primary_key=True)
    username = TextField()
    details = TextField()
    created_at = DatetimeField(auto_now_add=True)

    class Meta:
        table = 'audit_log'
