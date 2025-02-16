import uuid
from abc import ABC


class BaseId(ABC):
    def __init__(self):
        self.__value = uuid.uuid4()

    def __str__(self) -> str:
        return str(self.__value)

    def __eq__(self, other: "BaseId"):
        return self.__value == other.__value

    def __ne__(self, other: "BaseId"):
        return self.__value != other.__value

    def __repr__(self):
        return str(self.__value)

    def bytes(self):
        return self.__value.bytes  # Возвращаем байтовое представление UUID
