from pydantic import BaseModel


class Model(BaseModel):
    model_id: str
    model_path: str
