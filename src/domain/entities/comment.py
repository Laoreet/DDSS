from pydantic import BaseModel


class Comment(BaseModel):
    id: str
    ct_series_id: str
    author: str
    content: str
    timestamp: str
