from pydantic import BaseModel


class CTSeriesUploadedEvent(BaseModel):
    ct_series_id: str
    patient_id: str
    upload_date: str
