from pydantic import BaseModel
from typing import List
from fastapi import UploadFile


class UploadCTSeriesCommandDTO(BaseModel):
    ct_series_id: str
    patient_id: str
    files: List[UploadFile]


class AddCommentCommandDTO(BaseModel):
    comment_id: str
    ct_series_id: str
    author: str
    content: str


class GetProjectionsCommandDTO(BaseModel):
    ct_series_id: str
    projection_id: str
    axial: str
    sagital: str
    coronal: str


class CTSeriesUploadedEventDTO(BaseModel):
    ct_series_id: str
    patient_id: str
    upload_date: str


class CommentAddedEventDTO(BaseModel):
    ct_series_id: str
    comment_id: str
    author: str
    content: str
    timestamp: str


class ProjectionsBuildedEventDTO(BaseModel):
    ct_series_id: str
    projection_id: str
    axial: str
    sagital: str
    coronal: str
