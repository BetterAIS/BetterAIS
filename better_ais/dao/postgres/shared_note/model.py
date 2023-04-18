from tortoise.models import Model
from tortoise import fields


class SharedNote(Model):
    id = fields.IntField(pk=True)
    user_id = fields.IntField()
    content = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

     