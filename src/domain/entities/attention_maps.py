from pydantic import BaseModel


class AttentionMaps(BaseModel):
    id: str
    ct_series_id: str
    attention_map: str
