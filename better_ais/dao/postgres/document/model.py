from tortoise.models import Model
from tortoise import fields



class Document(Model):
    id = fields.IntField(pk=True)
    user_id = fields.IntField()
    subject = fields.CharField(max_length=255)
    title = fields.CharField(max_length=255)
    description = fields.TextField()
    file_path = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
