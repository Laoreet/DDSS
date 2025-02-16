from abc import ABC, abstractmethod
from domain.aggregates.ct_series_aggregate import CTSeriesAggregate
from typing import Optional


class ICTSeriesRepository(ABC):
    @abstractmethod
    async def save(self, ct_series_aggregate: "CTSeriesAggregate") -> None:
        """Сохраняет агрегат в БД."""
        pass

    @abstractmethod
    async def find_by_id(self, ct_series_id: str) -> Optional["CTSeriesAggregate"]:
        """Находит агрегат по ID."""
        pass

    @abstractmethod
    async def update(self, ct_series_aggregate: "CTSeriesAggregate") -> None:
        """Обновляет агрегат в БД."""
        pass
