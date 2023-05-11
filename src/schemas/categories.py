from datetime import datetime

from pydantic import BaseModel


class CategoryBase(BaseModel):
    id: int
    course_id: int
    name: str
    description: str
    active: bool
    date_created: datetime
    last_updated: datetime


class Category(CategoryBase):
    class Config:
        orm_mode = True
