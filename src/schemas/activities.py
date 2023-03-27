from datetime import datetime

from pydantic import BaseModel


class ActivityBase(BaseModel):
    id: int
    course_id: int
    activity_category_id: int
    name: str
    description: str
    language: str
    is_io_tested: bool
    points: int
    compilation_flags: str
    active: bool
    deleted: bool
    starting_files_id: int
    date_created: datetime
    last_updated: datetime


class Activity(ActivityBase):
    class Config:
        orm_mode = True
