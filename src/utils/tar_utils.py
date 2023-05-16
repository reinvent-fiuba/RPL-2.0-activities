from typing import List
import tarfile
import io

from fastapi import UploadFile

class TarUtils():
    def compressToTarGz(self, files: List[UploadFile]) -> bytes:
        fh = io.BytesIO()
        with tarfile.open(fileobj=fh, mode='w:gz') as tar:
            for file in files:
                info = tarfile.TarInfo(file.filename)
                info.size = file.size
                tar.addfile(info, file.file)

        return fh.getvalue()


