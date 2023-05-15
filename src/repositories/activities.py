from typing import List, Optional

from sqlmodel import select

from src.models.activities import Activity

from .main import AppRepository


class ActivitiesRepository(AppRepository):
    def create(self, activity: Activity) -> Activity:
        self.db.add(activity)
        self.db.commit()
        self.db.refresh(activity)
        return activity

    def get_by_course_id(self, course_id: int) -> List[Activity]:
        statement = select(Activity).where(Activity.course_id == course_id)
        activities = self.db.exec(statement).all()
        return activities

    def get_by_id(self, course_id: int, id: int) -> Activity:
        statement = select(Activity).where(Activity.course_id == course_id).where(Activity.id == id)
        activity = self.db.exec(statement).first()
        return activity

    def delete(self, course_id: int, id: int) -> Optional[Activity]:
        activity = self.get_by_id(course_id, id)
        if not activity:
            return None
        self.db.delete(activity)
        self.db.commit()
        return activity
        