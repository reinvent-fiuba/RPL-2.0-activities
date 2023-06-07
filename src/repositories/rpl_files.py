from typing import List, Optional

from sqlmodel import select

from src.models.rpl_files import RPLFile

from .main import AppRepository


class RPLFilesRepository(AppRepository):
    def create(self, rpl_file: RPLFile) -> RPLFile:
        self.db.add(rpl_file)
        self.db.commit()
        self.db.refresh(rpl_file)
        return rpl_file
