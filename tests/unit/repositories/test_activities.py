from unittest.mock import ANY, Mock

from src.models.activities import Activity
from src.repositories.activities import ActivitiesRepository


def test_get_by_course_id():
    course_id = "22"
    activities = [{"id": "1", "course_id": course_id}]

    db = Mock()
    db.query.return_value = db
    db.where.return_value = db
    db.all.return_value = activities

    res = ActivitiesRepository(db).get_by_course_id(course_id)

    # Should get the activities from the Activity table
    db.query.assert_called_once_with(Activity)

    # Should query by the course id
    db.where.assert_called_once_with(ANY)
    expected_query = Activity.course_id == course_id
    assert (
        db.where.call_args.args[0].right.effective_value
        == expected_query.right.effective_value
    )
    assert db.where.call_args.args[0].left == expected_query.left

    # Should return all the activities
    db.all.assert_called_once_with()

    # Should return the list of activities
    assert res == activities


def test_get_by_id():
    id = "1"
    course_id = "22"
    activity = {"id": id, "course_id": course_id}

    db = Mock()
    db.query.return_value = db
    db.where.return_value = db
    db.first.return_value = activity

    res = ActivitiesRepository(db).get_by_id(course_id, id)

    # Should get the activity from the Activity table
    db.query.assert_called_once_with(Activity)

    # Should query by the course id and id
    assert db.where.call_count == 2

    expected_query = Activity.course_id == course_id
    assert (
        db.where.mock_calls[0].args[0].right.effective_value
        == expected_query.right.effective_value
    )
    assert db.where.mock_calls[0].args[0].left == expected_query.left

    expected_query = Activity.id == id
    assert (
        db.where.mock_calls[1].args[0].right.effective_value
        == expected_query.right.effective_value
    )
    assert db.where.mock_calls[1].args[0].left == expected_query.left

    # Should return the first activity
    db.first.assert_called_once_with()

    # Should return the activity
    assert res == activity
