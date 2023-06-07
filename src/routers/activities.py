from typing import List

from fastapi import APIRouter, Depends

from src.config.database import get_db
from src.dependencies.authentication import authentication
from src.dependencies.authorization import authorization
from src.schemas.activities import Activity, ActivityCreate
from src.services.activities import ActivitiesService

router = APIRouter(
    prefix="/api/v2",
    tags=[],
    dependencies=[Depends(authentication), Depends(authorization)],
    responses={404: {"description": "Not found"}},
)


@router.post(
    "/courses/{course_id}/activities", status_code=201, response_model=Activity
)
async def create_activity(
    course_id: int, activity: ActivityCreate = Depends(), db: get_db = Depends()
):
    return ActivitiesService(db).create(course_id, activity)


@router.get("/courses/{course_id}/activities", response_model=List[Activity])
async def get_activities(course_id: int, db: get_db = Depends()):
    return ActivitiesService(db).get_by_course_id(course_id)


@router.get("/courses/{course_id}/activities/{activity_id}", response_model=Activity)
async def get_activity(course_id: int, activity_id: int, db: get_db = Depends()):
    return ActivitiesService(db).get_by_id(course_id, activity_id)


@router.delete("/courses/{course_id}/activities/{activity_id}", status_code=204)
async def delete_activity(course_id: int, activity_id: int, db: get_db = Depends()):
    return ActivitiesService(db).delete(course_id, activity_id)
