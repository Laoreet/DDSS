from utils.base_uuid import BaseId
from domain.entities.ct_series import CTSeriesId


class ModelResultsId(BaseId):
    pass


class ModelResults:
    def __init__(
        self,
        id: "ModelResultsId",
        ct_series_id: "CTSeriesId",
        hemorrhage_percent: float
    ):
        self.id = id
        self.ct_series_id = ct_series_id
        self.hemorrhage_percent = hemorrhage_percent

    def __eq__(self, other: "ModelResults"):
        return self.id == other.id

    def __ne__(self, other: "ModelResults"):
        return self.id != other.id
