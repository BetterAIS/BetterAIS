from tortoise.models import Model
from tortoise import fields


class UserSettings(Model):
    id = fields.IntField(pk=True)
    user_id = fields.IntField()
    setting_key = fields.CharField(max_length=255)
    setting_value = fields.CharField(max_length=255)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

     