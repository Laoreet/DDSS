from domain.entities.ct_series import CTSeries
from domain.entities.projections import Projections
from domain.entities.comment import Comment
from typing import List, Union
from utils.base_uuid import BaseId
from fastapi import UploadFile
import datetime


class CTSeriesAggregate:
    def __init__(self, ct_series: CTSeries, projections: Projections = None,
                 comments: List[Comment] = None):
        self.ct_series = ct_series
        self.projections = projections
        self.comments = comments or []

    def handle(self, command: "CTSeriesCommand") -> List["CTSeriesEvent"]:
        return self.handle_many([command])

    def handle_many(self, commands: List["CTSeriesCommand"]) -> List["CTSeriesEvent"]:
        events = []

        for command in commands:
            match command:
                case UploadCTSeriesCommand():
                    events.extend(self.__upload_ct_series(command))
                case AddCommentCommand():
                    events.extend(self.__add_comment(command))
                case GetProjectionsCommand():
                    events.extend(self.__get_projections(command))

    def __upload_ct_series(self, command: "UploadCTSeriesCommand") -> List["CTSeriesEvent"]:
        event = CTSeriesUploadedEvent(
            ct_series_id=command.ct_series_id,
            patient_id=command.patient_id,
            upload_date=str(datetime.datetime.now()),
        )
        return [event]

    def __add_comment(self, command: "AddCommentCommand") -> List["CTSeriesEvent"]:
        event = CommentAddedEvent(
            ct_series_id=command.ct_series_id,
            comment_id=command.comment_id,
            author=command.author,
            content=command.content,
            timestamp=str(datetime.datetime.now()),
        )
        return [event]

    def __get_projections(self, command: "GetProjectionsCommand") -> List["CTSeriesEvent"]:
        event = ProjectionsBuildedEvent(
            ct_series_id=command.ct_series_id,
            projection_id=command.projection_id,
            axial=command.axial,
            sagital=command.sagital,
            coronal=command.coronal,
        )
        return [event]


CTSeriesCommand = Union[
    "UploadCTSeriesCommand",
    "AddCommentCommand",
    "GetProjectionsCommand",
]

CTSeriesEvent = Union[
    "CTSeriesUploadedEvent",
    "CommentAddedEvent",
    "ProjectionsBuildedEvent",
]


# Events


class CTSeriesUploadedEvent:
    ct_series_id: "BaseId"
    patient_id: str
    upload_date: str


class CommentAddedEvent:
    ct_series_id: "BaseId"
    comment_id: "BaseId"
    author: str
    content: str
    timestamp: str


class ProjectionsBuildedEvent:
    ct_series_id: "BaseId"
    projection_id: "BaseId"
    axial: str = 'заглушка axial'
    sagital: str = 'заглушка sagital'
    coronal: str = 'заглушка coronal'


# Commands


class UploadCTSeriesCommand:
    ct_series_id: "BaseId"
    patient_id: str
    files: List[UploadFile]


class AddCommentCommand:
    comment_id: "BaseId"
    ct_series_id: "BaseId"
    author: str
    content: str


class GetProjectionsCommand:
    ct_series_id: "BaseId"
    projection_id: "BaseId"
    axial: str
    sagital: str
    coronal: str
