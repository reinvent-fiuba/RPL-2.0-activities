from typing import List

from fastapi import APIRouter, Depends

from src.config.database import get_db
from src.dependencies.authentication import authentication
from src.dependencies.authorization import authorization
from src.schemas.categories import Category
from src.services.categories import CategoriesService

router = APIRouter(
    prefix="/api/v2",
    tags=[],
    dependencies=[Depends(authentication), Depends(authorization)],
    responses={404: {"description": "Not found"}},
)


@router.get("/courses/{course_id}/categories", response_model=List[Category])
async def get_categories(course_id: int, db: get_db = Depends()):
    result = CategoriesService(db).get_by_course_id(course_id)
    return result


@router.get("/courses/{course_id}/categories/{category_id}", response_model=Category)
async def get_category(course_id: int, category_id: int, db: get_db = Depends()):
    result = CategoriesService(db).get_by_id(course_id, category_id)
    return result
