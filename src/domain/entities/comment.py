from utils.base_uuid import BaseId
from domain.entities.ct_series import CTSeriesId


class CommentId(BaseId):
    pass


class Comment:
    def __init__(
        self,
        id: CommentId,
        ct_series_id: "CTSeriesId",
        author: str,
        content: str,
        timestamp: str
    ):
        self.id = id
        self.ct_series_id = ct_series_id
        self.author = author
        self.content = content
        self.timestamp = timestamp

    def __eq__(self, other: "Comment"):
        return self.id == other.id

    def __ne__(self, other: "Comment"):
        return self.id != other.id
