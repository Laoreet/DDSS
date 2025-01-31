from pydantic import BaseModel


class Projections(BaseModel):
    id: str
    ct_series_id: str
    axial: str
    sagital: str
    coronal: str
