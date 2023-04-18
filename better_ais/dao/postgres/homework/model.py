from tortoise.models import Model
from tortoise import fields



class Homework(Model):
    id = fields.IntField(pk=True)
    user_id = fields.IntField()
    subject_id = fields.IntField()
    title = fields.CharField(max_length=255)
    description = fields.TextField()
    mark = fields.IntField()
    link = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

