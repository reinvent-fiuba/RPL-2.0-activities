from typing import List

from fastapi import HTTPException

from src.models.activities import Activity
from src.models.rpl_files import RPLFile
from src.repositories.activities import ActivitiesRepository
from src.services.main import AppService
from src.services.rpl_files import RPLFilesService
from src.services.categories import CategoriesService
from src.schemas.activities import ActivityCreate

from datetime import datetime

class ActivitiesService(AppService):
    def create(self, course_id: int, activity: ActivityCreate) -> Activity:
        # Just try to get the category, to validate its existence within the course
        CategoriesService(self.db).get_by_id(course_id, activity.activity_category_id)

        file = RPLFile(
            file_name=f"{datetime.now()}_{course_id}_{activity.name}.tar.gz",
            file_type="application/gzip",
            data=activity.starting_file,
            date_created=datetime.now(),
            last_updated=datetime.now()
        )

        file = RPLFilesService(self.db).create(file)

        activity = ActivitiesRepository(self.db).create(activity.to_activity(course_id, file.id))
        return activity
    
    def get_by_course_id(self, course_id: int) -> List[Activity]:
        activities = ActivitiesRepository(self.db).get_by_course_id(course_id)
        return activities

    def get_by_id(self, course_id: int, id: int) -> Activity:
        activity = ActivitiesRepository(self.db).get_by_id(course_id, id)
        if not activity:
            raise HTTPException(
                status_code=404,
                detail=f"The Activity with ID {id} does not exist in the Course {course_id}",
            )
        return activity

    def delete(self, course_id: int, id: int):
        activity = ActivitiesRepository(self.db).delete(course_id, id)
        if not activity:
            raise HTTPException(
                status_code=404,
                detail=f"The Activity with ID {id} does not exist in the Course {course_id}",
            )
        
