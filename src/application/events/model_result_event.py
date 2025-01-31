from pydantic import BaseModel


class ModelResultEvent(BaseModel):
    model_id: str
    ct_series_id: str
    hemorrhage_percent: float
