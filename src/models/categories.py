from sqlmodel import Field, SQLModel

from src.schemas.categories import CategoryBase


class Category(SQLModel, CategoryBase, table=True):
    __tablename__ = "activity_categories"

    id: int = Field(None, primary_key=True, index=True)
