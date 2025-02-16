from utils.base_uuid import BaseId
from domain.entities.ct_series import CTSeriesId


class ProjectionsId(BaseId):
    pass


class Projections:
    def __init__(
        self,
        id: ProjectionsId,
        ct_series_id: "CTSeriesId",
        axial: str,
        sagital: str,
        coronal: str
    ):
        self.id = id
        self.ct_series_id = ct_series_id
        self.axial = axial
        self.sagital = sagital
        self.coronal = coronal

    def __eq__(self, other: "Projections"):
        return self.id == other.id

    def __ne__(self, other: "Projections"):
        return self.id != other.id
