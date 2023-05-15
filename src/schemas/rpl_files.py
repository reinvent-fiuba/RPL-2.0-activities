from datetime import datetime

from pydantic import BaseModel

class RPLFileBase(BaseModel):
    id: int
    file_name: str
    file_type: str
    data: bytes
    date_created: datetime
    last_updated: datetime


class RPLFile(RPLFileBase):
    class Config:
        orm_mode = True
