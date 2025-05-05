import uuid
from tortoise.models import Model
from tortoise import fields


class User(Model):
    id = fields.UUIDField(primary_key=True, default=uuid.uuid4)
    descope_user_id = fields.CharField(max_length=100, unique=True)
    email = fields.CharField(max_length=255)
    created_at = fields.DatetimeField(auto_now_add=True)
    is_banned = fields.BooleanField(default=False)
    role = fields.ForeignKeyField("models.Role", related_name="users")
