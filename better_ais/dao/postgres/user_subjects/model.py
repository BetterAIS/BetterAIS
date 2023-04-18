from tortoise.models import Model
from tortoise import fields

    
class UserSubject(Model):
    id = fields.IntField(pk=True)
    user_id = fields.IntField()
    subject_id = fields.IntField()
    year = fields.IntField()
    semester = fields.IntField()
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    
     