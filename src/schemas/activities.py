from datetime import datetime

from pydantic import BaseModel

from typing import Optional, List

from fastapi import Form, UploadFile

from src.utils.tar_utils import TarUtils

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

class ActivityCreate():
    def __init__(
        self,
        activityCategoryId: int = Form(),
        name: str = Form(),
        description: str = Form(),
        language: str = Form(),
        points: int = Form(),
        compilationFlags: Optional[str] = Form(default=""),
        active: Optional[bool] = Form(default=True),
        startingFile: List[UploadFile] = Form()
    ):
        self.activity_category_id = activityCategoryId
        self.name = name
        self.description = description
        self.language = language
        self.points = points
        self.compilation_flags = compilationFlags
        self.active = active
        self.starting_file = TarUtils().compressToTarGz(startingFile) # Compress files and store bytes

    def to_activity(self, course_id, starting_files_id):
        # This is not a good practice, doing it here just to avoid circular dependency
        from src.models.activities import Activity as ActivityModel

        date_created=datetime.now()

        return ActivityModel(
            activity_category_id = self.activity_category_id,
            name = self.name,
            description = self.description,
            language = self.language,
            points = self.points,
            compilation_flags = self.compilation_flags,
            active = self.active,
            
            course_id=course_id,
            starting_files_id=starting_files_id,

            is_io_tested=True,
            deleted=False,

            date_created=date_created,
            last_updated=date_created,
        )

# startingFiles = startingFiles;
