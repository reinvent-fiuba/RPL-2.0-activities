from unittest.mock import patch

from fastapi import HTTPException

from src.repositories.activities import ActivitiesRepository
from src.services.activities import ActivitiesService


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
