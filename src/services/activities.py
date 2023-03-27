from src.repositories.activities import ActivitiesRepository
from src.services.main import AppService


class ActivitiesService(AppService):
    def get_by_course_id(self, course_id: int):
        activities = ActivitiesRepository(self.db).get_by_course_id(course_id)
        return activities
