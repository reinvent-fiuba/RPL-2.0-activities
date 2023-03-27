from sqlmodel import Field, SQLModel

from src.schemas.activities import ActivityBase


class Activity(SQLModel, ActivityBase, table=True):
    __tablename__ = "activities"

    id: int = Field(None, primary_key=True, index=True)
