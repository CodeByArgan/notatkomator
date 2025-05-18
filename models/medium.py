import uuid
from enum import Enum
from tortoise.models import Model
from tortoise import fields


class MediumType(str, Enum):
    BOOK = "book"
    MOVIE = "movie"
    SHOW = "show"
    GAME = "game"
    ALBUM = "album"
    COMIC = "comic"


class Medium(Model):
    id = fields.UUIDField(primary_key=True, default=uuid.uuid4)
    name = fields.CharField(max_length=1024, unique=True)
    type = fields.CharEnumField(MediumType)
    image = fields.CharField(max_length=1024, null=True, default=None)
    description = fields.CharField(max_length=2048, null=True, default="")
    is_public = fields.BooleanField(default=False)
    is_removed = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(auto_now_add=True)
    last_edit_at = fields.DatetimeField(default=None, null=True)
    creator = fields.ForeignKeyField("models.User", related_name="medium_creator")

