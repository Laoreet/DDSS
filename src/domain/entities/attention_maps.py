from ct_series import CTSeriesId
from utils.base_uuid import BaseId


class AttentionMapId(BaseId):
    pass


class AttentionMaps:
    def __init__(self, id: "AttentionMapId", ct_series_id: "CTSeriesId", attention_map: str):
        self.id = id
        self.ct_series_id = ct_series_id
        self.attention_map = attention_map

    def __eq__(self, other: "AttentionMaps"):
        return self.id == other.id

    def __ne__(self, other: "AttentionMaps"):
        return self.id != other.id
