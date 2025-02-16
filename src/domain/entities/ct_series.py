from typing import List, Optional
from utils.base_uuid import BaseId
from datetime import datetime


class CTSeriesId(BaseId):
    pass


class CTSeries:
    def __init__(
        self,
        id: CTSeriesId,
        patient_id: str,
        upload_date: datetime,
        status: str,
        comments: List[str] = [],
        hemorrhage_percent: Optional[float] = None,
        projections: Optional[List[str]] = None,
        attention_maps: Optional[List[str]] = None
    ):
        self.id = id
        self.patient_id = patient_id
        self.upload_date = upload_date
        self.status = status
        self.comments = comments
        self.hemorrhage_percent = hemorrhage_percent
        self.projections = projections
        self.attention_maps = attention_maps

    def __eq__(self, other: "CTSeries"):
        return self.id == other.id

    def __ne__(self, other: "CTSeries"):
        return self.id != other.id
