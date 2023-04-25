from tortoise.models import Model
from tortoise import fields


class Mail(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="mails")
    sender = fields.CharField(max_length=255)
    subject = fields.CharField(max_length=255)
    body = fields.TextField()
    is_read = fields.BooleanField()
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

