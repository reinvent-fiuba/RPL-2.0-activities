from sqlmodel import Field, SQLModel

from typing import Optional

from src.schemas.rpl_files import RPLFileBase


class RPLFile(SQLModel, RPLFileBase, table=True):
    __tablename__ = "rpl_files"

    id: int = Field(None, primary_key=True, index=True)
