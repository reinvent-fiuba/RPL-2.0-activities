from src.models.activities import Activity

from .main import AppRepository


class ActivitiesRepository(AppRepository):
    def get_by_course_id(self, course_id: int):
        activities = (
            self.db.query(Activity).filter(Activity.course_id == course_id).all()
        )
        return activities
