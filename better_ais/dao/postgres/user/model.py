from tortoise.models import Model
from tortoise import fields


class User(Model):
    id = fields.IntField(pk=True)
    ais_id = fields.IntField()
    ais_username = fields.TextField()
    password_hash = fields.TextField()
    password_salt = fields.TextField()
    is_verified = fields.BooleanField()
    totp_secret = fields.TextField()
    email = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

     