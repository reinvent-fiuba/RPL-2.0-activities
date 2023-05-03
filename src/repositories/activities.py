from typing import List

from src.models.activities import Activity

from .main import AppRepository


class ActivitiesRepository(AppRepository):
    def get_by_course_id(self, course_id: int) -> List[Activity]:
        activities = (
            self.db.query(Activity).where(Activity.course_id == course_id).all()
        )
        return activities

    def get_by_id(self, course_id: int, id: int) -> Activity:
        activity = (
            self.db.query(Activity)
            .where(Activity.course_id == course_id)
            .where(Activity.id == id)
            .first()
        )
        return activity
