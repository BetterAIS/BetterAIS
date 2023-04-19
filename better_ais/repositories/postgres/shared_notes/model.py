from tortoise.models import Model
from tortoise import fields


class SharedNote(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="shared_notes")
    content = fields.TextField() # is encrypted like obsidian extension named "Obsidian Sync"
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

     