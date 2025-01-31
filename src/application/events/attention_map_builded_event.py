from pydantic import BaseModel


class AttentionMapBuildedEvent(BaseModel):
    ct_series_id: str
    attention_map_id: str
    attention_map: str
