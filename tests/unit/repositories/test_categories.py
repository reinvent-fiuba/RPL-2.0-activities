from unittest.mock import ANY, Mock

from src.models.categories import Category
from src.repositories.categories import CategoriesRepository


def test_get_by_course_id():
    course_id = "22"
    categories = [{"id": "1", "course_id": course_id}]

    db = Mock()
    db.query.return_value = db
    db.where.return_value = db
    db.all.return_value = categories

    res = CategoriesRepository(db).get_by_course_id(course_id)

    # Should get the categories from the categories table
    db.query.assert_called_once_with(Category)

    # Should query by the course id
    db.where.assert_called_once_with(ANY)
    expected_query = Category.course_id == course_id
    assert (
        db.where.call_args.args[0].right.effective_value
        == expected_query.right.effective_value
    )
    assert db.where.call_args.args[0].left == expected_query.left

    # Should return all the categories
    db.all.assert_called_once_with()

    # Should return the list of categories
    assert res == categories


def test_get_by_id():
    id = "1"
    course_id = "22"
    category = {"id": id, "course_id": course_id}

    db = Mock()
    db.query.return_value = db
    db.where.return_value = db
    db.first.return_value = category

    res = CategoriesRepository(db).get_by_id(course_id, id)

    # Should get the category from the Category table
    db.query.assert_called_once_with(Category)

    # Should query by the course id and id
    assert db.where.call_count == 2

    expected_query = Category.course_id == course_id
    assert (
        db.where.mock_calls[0].args[0].right.effective_value
        == expected_query.right.effective_value
    )
    assert db.where.mock_calls[0].args[0].left == expected_query.left

    expected_query = Category.id == id
    assert (
        db.where.mock_calls[1].args[0].right.effective_value
        == expected_query.right.effective_value
    )
    assert db.where.mock_calls[1].args[0].left == expected_query.left

    # Should return the first category
    db.first.assert_called_once_with()

    # Should return the category
    assert res == category
