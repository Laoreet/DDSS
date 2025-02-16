from infrastructure.ct_series_repository_base import ICTSeriesRepository
from domain.entities.ct_series import CTSeries
from domain.aggregates.ct_series_aggregate import (
    CTSeriesAggregate,
    UploadCTSeriesCommand
    )
from datetime import datetime


class ApplicationService:
    def __init__(self, ct_series_repository: ICTSeriesRepository):
        self.ct_series_repository = ct_series_repository

    async def upload_ct_series(self,
                               cmd: UploadCTSeriesCommand) -> CTSeriesAggregate:
        # Создаем агрегат
        ct_series = CTSeries(
            id=cmd.ct_series_id,
            patient_id=cmd.patient_id,
            upload_date=str(datetime.datetime.now()),
            status="pending",
        )
        aggregate = CTSeriesAggregate(ct_series=ct_series)

        # Сохраняем в БД
        await self.ct_series_repository.save(aggregate)
        return aggregate
