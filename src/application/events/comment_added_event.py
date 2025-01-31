from pydantic import BaseModel


class CommentAddedEvent(BaseModel):
    ct_series_id: str
    comment_id: str
    author: str
    content: str
    timestamp: str
