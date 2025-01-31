from pydantic import BaseModel
from typing import List, Optional


class CTSeries(BaseModel):
    id: str
    patient_id: str
    upload_date: str
    status: str
    comments: List[str] = []
    hemorrhage_percent: Optional[float] = None
    projections: Optional[List[str]] = None
    attention_maps: Optional[List[str]] = None
