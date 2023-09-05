from typing import List

from fastapi import HTTPException

from src.models.rpl_files import RPLFile
from src.repositories.rpl_files import RPLFilesRepository
from src.services.main import AppService


class RPLFilesService(AppService):
    def create(self, file: RPLFile) -> RPLFile:
        file = RPLFilesRepository(self.db).create(file)
        return file
