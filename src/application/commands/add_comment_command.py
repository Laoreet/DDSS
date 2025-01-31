from pydantic import BaseModel


class AddCommentCommand(BaseModel):
    ct_series_id: str
    author: str
    content: str
