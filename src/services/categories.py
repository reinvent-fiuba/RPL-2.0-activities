from typing import List

from fastapi import HTTPException

from src.models.categories import Category
from src.repositories.categories import CategoriesRepository
from src.services.main import AppService


class CategoriesService(AppService):
    def get_by_course_id(self, course_id: int) -> List[Category]:
        categories = CategoriesRepository(self.db).get_by_course_id(course_id)
        return categories

    def get_by_id(self, course_id: int, id: int) -> Category:
        category = CategoriesRepository(self.db).get_by_id(course_id, id)
        if not category:
            raise HTTPException(
                status_code=404,
                detail=f"The Category with ID {id} does not exist in the Course {course_id}",
            )
        return category
