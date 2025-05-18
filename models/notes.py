import uuid
from enum import Enum
from tortoise.models import Model
from tortoise import fields

class NoteStatus(str, Enum):
    BACKLOG = "backlog"
    IN_BETWEEN = "in_between"
    DONE = "done"


class Note(Model):
    id = fields.UUIDField(primary_key=True, default=uuid.uuid4)
    user = fields.ForeignKeyField("models.User", related_name="note_owner")
    score = fields.IntField(min=0, max=10, default=0)
    status = fields.CharEnumField(NoteStatus, default=NoteStatus.BACKLOG)
    medium = fields.ForeignKeyField("models.Medium", related_name="note_medium")
    note = fields.CharField(max_length=1024, null=True, default="")
    is_removed = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(auto_now_add=True)
    last_edit_at = fields.DatetimeField(default=None, null=True)    

    