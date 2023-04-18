from tortoise.models import Model
from tortoise import fields


class Mail(Model):
    id = fields.IntField(pk=True)
    recipient_id = fields.IntField()
    sender_id = fields.IntField()
    subject = fields.CharField(max_length=255)
    body = fields.TextField()
    is_read = fields.BooleanField()
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

