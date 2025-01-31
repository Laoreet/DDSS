from pydantic import BaseModel


class GetProjectionsCommand(BaseModel):
    ct_series_id: str
