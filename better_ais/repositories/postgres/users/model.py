from tortoise.models import Model
from tortoise import fields


class User(Model):
    id = fields.IntField(pk=True)
    ais_username = fields.TextField()
    is_verified = fields.BooleanField()
    totp_secret = fields.TextField(default=None, null=True)
    email = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    roles = fields.ManyToManyField("models.Role", related_name="users", through="user_roles")
    shared_notes = fields.ReverseRelation["models.SharedNote"]
    posts = fields.ReverseRelation["models.Post"]
    mails = fields.ReverseRelation["models.Mail"]


