from pydantic import BaseModel
from typing import List
from fastapi import UploadFile


class UploadCTSeriesCommand(BaseModel):
    patient_id: str
    files: List[UploadFile]
