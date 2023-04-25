from tortoise.models import Model
from tortoise import fields


class Document(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField('models.User', related_name='documents')
    author = fields.CharField(max_length=255)
    subject = fields.CharField(max_length=255)
    title = fields.CharField(max_length=255)
    description = fields.TextField()
    file_path = fields.CharField(max_length=255)
    link = fields.CharField(max_length=255)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
