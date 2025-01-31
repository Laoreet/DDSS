from pydantic import BaseModel


class ModelResults(BaseModel):
    id: str
    ct_series_id: str
    hemorrhage_percent: float
