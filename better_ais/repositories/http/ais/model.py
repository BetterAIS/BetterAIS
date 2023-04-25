import datetime

from pydantic import BaseModel


class Mail(BaseModel):
    id: int
    user: int
    sender: str
    subject: str
    body: str
    is_read: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime

class Document(BaseModel):
    id: int
    user: int
    author: str
    subject: str
    title: str
    description: str
    file_path: str
    link: str
    created_at: datetime.datetime
    updated_at: datetime.datetime

class Homework(BaseModel):
    id: int
    user: int
    title: str
    description: str
    link: str
    created_at: datetime.datetime
    updated_at: datetime.datetime

class TimeTable(BaseModel):
    user: int
    day: str
    lesson: str
    time: str
    teacher: str
    room: str
