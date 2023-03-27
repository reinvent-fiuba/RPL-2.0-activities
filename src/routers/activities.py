from typing import List

from fastapi import APIRouter, Depends

from src.config.database import get_db
from src.schemas.activities import Activity
from src.services.activities import ActivitiesService

router = APIRouter(
    prefix="/api/v2",
    tags=[],
    responses={404: {"description": "Not found"}},
)


@router.get("/courses/{course_id}/activities", response_model=List[Activity])
async def get_activities(course_id: int, db: get_db = Depends()):
    result = ActivitiesService(db).get_by_course_id(course_id)
    return result
