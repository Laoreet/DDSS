from pydantic import BaseModel


class GetAttentionMapsCommand(BaseModel):
    ct_series_id: str
    model_id: str
