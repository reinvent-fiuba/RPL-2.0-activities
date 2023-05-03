from typing import List

from fastapi import HTTPException

from src.models.activities import Activity
from src.repositories.activities import ActivitiesRepository
from src.services.main import AppService


class ActivitiesService(AppService):
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
