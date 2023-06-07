from unittest.mock import Mock

from src.repositories.rpl_files import RPLFilesRepository

def test_create():
    file = {"id": "1"}

    db = Mock()
    db.add.return_value = db
    db.commit.return_value = db
    db.refresh.return_value = file

    res = RPLFilesRepository(db).create(file)

    # Should create the file
    db.add.assert_called_once_with(file)

    # Should commit the transaction
    db.commit.assert_called_once_with()

    # Should refresh the file object
    db.refresh.assert_called_once_with(file)

    # Should return the activity
    assert res == file
