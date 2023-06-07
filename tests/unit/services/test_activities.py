from unittest.mock import patch

from fastapi import HTTPException

from src.models.activities import Activity
from src.models.rpl_files import RPLFile
from src.repositories.activities import ActivitiesRepository
from src.schemas.activities import ActivityCreate
from src.services.activities import ActivitiesService
from src.services.categories import CategoriesService
from src.services.rpl_files import RPLFilesService


@patch.object(ActivitiesRepository, "get_by_course_id")
def test_get_by_course_id(get_by_course_id_mock):
    course_id = "22"
    activities = [{"id": "1", "course_id": course_id}]
    ActivitiesRepository.get_by_course_id.return_value = activities

    res = ActivitiesService({}).get_by_course_id(course_id)

    # Should get the activities by course id
    ActivitiesRepository.get_by_course_id.assert_called_once_with(course_id)

    # Should return the list of activities
    assert activities == res


@patch.object(ActivitiesRepository, "get_by_id")
def test_get_by_id(get_by_id_mock):
    course_id = "22"
    id = "1"
    activity = [{"id": id, "course_id": course_id}]
    ActivitiesRepository.get_by_id.return_value = activity

    res = ActivitiesService({}).get_by_id(course_id, id)

    # Should get the activity by course id and id
    ActivitiesRepository.get_by_id.assert_called_once_with(course_id, id)

    # Should return the activity
    assert activity == res


@patch.object(ActivitiesRepository, "get_by_id")
def test_get_by_id_not_found(get_by_id_mock):
    course_id = "22"
    id = "1"
    ActivitiesRepository.get_by_id.return_value = None

    try:
        ActivitiesService({}).get_by_id(course_id, id)
    except HTTPException as err:
        error = err

    # Should get the activity by course id and id
    ActivitiesRepository.get_by_id.assert_called_once_with(course_id, id)

    # Should raise a not found error
    assert error.status_code == 404
    assert (
        error.detail
        == f"The Activity with ID {id} does not exist in the Course {course_id}"
    )


@patch.object(ActivitiesRepository, "create")
@patch.object(RPLFilesService, "create")
@patch.object(CategoriesService, "get_by_id")
@patch.object(ActivityCreate, "to_activity")
def test_create_activity(
    create_activity_mock, create_file_mock, get_by_id_mock, to_activity_mock
):
    course_id = "22"
    activity_create = ActivityCreate(
        activityCategoryId="1",
        name="Test Activity",
        description="Some Description",
        language="Python",
        points=22,
        startingFile=[],
    )

    # Mock file creation
    file_id = "15"

    def create_file(file):
        file.id = file_id
        return file

    RPLFilesService.create.side_effect = create_file

    # Mock activity creation
    def to_activity(course_id, file_id):
        return Activity(
            activity_category_id=activity_create.activity_category_id,
            name=activity_create.name,
            description=activity_create.description,
            language=activity_create.language,
            points=activity_create.points,
            course_id=course_id,
            starting_files_id=file_id,
        )

    ActivityCreate.to_activity.side_effect = to_activity
    activity = to_activity(course_id, file_id)
    ActivitiesRepository.create.return_value = activity

    res = ActivitiesService({}).create(course_id, activity_create)

    # Should create the file
    RPLFilesService.create.assert_called_once()

    # Should create the activity
    ActivitiesRepository.create.assert_called_once_with(activity)

    # Should return the activity
    assert activity == res


@patch.object(ActivitiesRepository, "delete")
def test_delete_activity(delete_mock):
    course_id = "22"
    id = "1"
    activity = {"id": id, "course_id": course_id}
    ActivitiesRepository.delete.return_value = activity

    ActivitiesService({}).delete(course_id, id)

    # Should delete the activity
    ActivitiesRepository.delete.assert_called_once_with(course_id, id)


@patch.object(ActivitiesRepository, "delete")
def test_delete_activity_not_found(delete_mock):
    course_id = "22"
    id = "1"
    ActivitiesRepository.delete.return_value = None

    try:
        ActivitiesService({}).delete(course_id, id)
    except HTTPException as err:
        error = err

    # Should raise a not found error
    assert error.status_code == 404
    assert (
        error.detail
        == f"The Activity with ID {id} does not exist in the Course {course_id}"
    )
