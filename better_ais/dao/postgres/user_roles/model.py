from tortoise.models import Model
from tortoise import fields


class UserRoles(Model):
    id = fields.IntField(pk=True)
    user_id = fields.IntField()
    role_id = fields.IntField()
    is_public = fields.BooleanField()
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

     