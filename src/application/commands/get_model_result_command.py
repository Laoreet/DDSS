from pydantic import BaseModel


class GetModelResultCommand(BaseModel):
    ct_series_id: str
    model_id: str
