from unittest.mock import patch

from fastapi import HTTPException

from src.repositories.categories import CategoriesRepository
from src.services.categories import CategoriesService


@patch.object(CategoriesRepository, "get_by_course_id")
def test_get_by_course_id(get_by_course_id_mock):
    course_id = "22"
    categories = [{"id": "1", "course_id": course_id}]
    CategoriesRepository.get_by_course_id.return_value = categories

    res = CategoriesService({}).get_by_course_id(course_id)

    # Should get the categories by course id
    CategoriesRepository.get_by_course_id.assert_called_once_with(course_id)

    # Should return the list of categories
    assert categories == res


@patch.object(CategoriesRepository, "get_by_id")
def test_get_by_id(get_by_id_mock):
    course_id = "22"
    id = "1"
    category = {"id": id, "course_id": course_id}
    CategoriesRepository.get_by_id.return_value = category

    res = CategoriesService({}).get_by_id(course_id, id)

    # Should get the category by course id and id
    CategoriesRepository.get_by_id.assert_called_once_with(course_id, id)

    # Should return the category
    assert category == res


@patch.object(CategoriesRepository, "get_by_id")
def test_get_by_id_not_found(get_by_id_mock):
    course_id = "22"
    id = "1"
    CategoriesRepository.get_by_id.return_value = None

    try:
        CategoriesService({}).get_by_id(course_id, id)
    except HTTPException as err:
        error = err

    # Should get the category by course id and id
    CategoriesRepository.get_by_id.assert_called_once_with(course_id, id)

    # Should raise a not found error
    assert error.status_code == 404
    assert (
        error.detail
        == f"The Category with ID {id} does not exist in the Course {course_id}"
    )
