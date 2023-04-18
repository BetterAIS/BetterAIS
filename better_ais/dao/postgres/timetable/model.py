from tortoise.models import Model
from tortoise import fields


class Timetable(Model):
    id = fields.IntField(pk=True)
    user_id = fields.IntField()
    subject_id = fields.IntField()
    day = fields.CharField(max_length=255)
    start_time = fields.CharField(max_length=255)
    end_time = fields.CharField(max_length=255)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

     