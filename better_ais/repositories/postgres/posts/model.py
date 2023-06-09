from tortoise.models import Model
from tortoise import fields


class Post(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="posts")
    title = fields.CharField(max_length=255)
    content = fields.TextField()
    documents = fields.JSONField()
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

     