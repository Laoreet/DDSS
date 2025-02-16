from domain.entities.model import Model
from domain.entities.model_results import ModelResults
from domain.entities.attention_maps import AttentionMaps
from typing import List, Union
from utils.base_uuid import BaseId


class ModelAggregate:
    def __init__(
        self,
        model: Model,
        model_results: ModelResults = None,
        attention_maps: AttentionMaps = None
    ):
        self.model = model
        self.model_results = model_results
        self.attention_maps = attention_maps or []

    def handle(self, command: "ModelCommand") -> List["ModelEvent"]:
        return self.handle_many([command])

    def handle_many(self, commands: List["ModelCommand"]) -> List["ModelEvent"]:
        events = []

        for command in commands:
            match command:
                case GetAttentionMapsCommand():
                    events.extend(self.__get_attention_maps(command))
                case GetModelResultCommand():
                    events.extend(self.__get_model_result(command))

        return events

    def __get_attention_maps(self, command: "GetAttentionMapsCommand") -> List["ModelEvent"]:
        event = AttentionMapBuildedEvent(
            ct_series_id=command.ct_series_id,
            attention_map_id=str(BaseId()),  # Генерация нового ID для attention_map
            attention_map="заглушка attention_map"  # Заглушка для примера
        )
        return [event]

    def __get_model_result(self, command: "GetModelResultCommand") -> List["ModelEvent"]:
        event = ModelResultEvent(
            model_id=command.model_id,
            ct_series_id=command.ct_series_id,
            hemorrhage_percent=13.37  # Заглушка для примера
        )
        return [event]


ModelCommand = Union[
    "GetAttentionMapsCommand",
    "GetModelResultCommand",
]

ModelEvent = Union[
    "AttentionMapBuildedEvent",
    "ModelResultEvent",
]


# Events


class AttentionMapBuildedEvent:
    ct_series_id: "BaseId"
    attention_map_id: "BaseId"
    attention_map: str


class ModelResultEvent:
    model_id: "BaseId"
    ct_series_id: "BaseId"
    hemorrhage_percent: float


# Commands


class GetAttentionMapsCommand:
    ct_series_id: "BaseId"
    model_id: "BaseId"


class GetModelResultCommand:
    ct_series_id: "BaseId"
    model_id: "BaseId"
