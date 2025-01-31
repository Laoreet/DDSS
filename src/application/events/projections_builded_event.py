from pydantic import BaseModel


class ProjectionsBuildedEvent(BaseModel):
    ct_series_id: str
    projection_id: str
    axial: str
    sagital: str
    coronal: str
