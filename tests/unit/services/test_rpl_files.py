from unittest.mock import Mock, patch

from src.repositories.rpl_files import RPLFilesRepository
from src.services.rpl_files import RPLFilesService


@patch.object(RPLFilesRepository, "create")
def test_create_rpl_file(create_mock):
    file = Mock()
    RPLFilesRepository.create.return_value = file

    res = RPLFilesService({}).create(file)

    # Should create the rpl file
    RPLFilesRepository.create.assert_called_once_with(file)

    # Should return the rpl file
    assert file == res
