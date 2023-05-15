from typing import List

from src.models.categories import Category

from .main import AppRepository


class CategoriesRepository(AppRepository):
    def get_by_course_id(self, course_id: int) -> List[Category]:
        categories = (
            self.db.query(Category).where(Category.course_id == course_id).all()
        )
        return categories

    def get_by_id(self, course_id: int, id: int) -> Category:
        category = (
            self.db.query(Category)
            .where(Category.course_id == course_id)
            .where(Category.id == id)
            .first()
        )
        return category
