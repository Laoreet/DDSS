import asyncpg
from domain.aggregates.ct_series_aggregate import CTSeriesAggregate
from domain.entities.ct_series import CTSeries
from domain.entities.projections import Projections
from domain.entities.comment import Comment
from typing import Optional
from infrastructure.ct_series_repository_base import ICTSeriesRepository


class PostgreSQLCTSeriesRepository(ICTSeriesRepository):
    def __init__(self, connection: asyncpg.Connection):
        self.connection = connection

    async def save(self, ct_series_aggregate: "CTSeriesAggregate") -> None:
        """Сохраняет агрегат в БД."""
        # Сохраняем CTSeries
        await self.connection.execute(
            """
            INSERT INTO ct_series (id, patient_id, upload_date, status)
            VALUES ($1, $2, $3, $4)
            """,
            str(ct_series_aggregate.ct_series.id),
            ct_series_aggregate.ct_series.patient_id,
            ct_series_aggregate.ct_series.upload_date,
            ct_series_aggregate.ct_series.status,
        )

        # # Сохраняем сами наши файлы дикомовские
        # study_folder = os.path.join(UPLOAD_FOLDER, ct_series_aggregate.ct_series.id)
        # os.makedirs(study_folder, exist_ok=True)

        # for file in ct_series_aggregate.files:
        #     if not file.filename.endswith(".dcm"):
        #         raise Exception("Invalid file format. Expected DICOM.")
        #     file_path = os.path.join(study_folder, file.filename)
        #     with open(file_path, "wb") as f:
        #         f.write(await file.read())

        # Сохраняем Projections (если есть)
        if ct_series_aggregate.projections:
            await self.connection.execute(
                """
                INSERT INTO projections (id, axial, sagital, coronal)
                VALUES ($1, $2, $3, $4)
                """,
                ct_series_aggregate.projections.id,
                ct_series_aggregate.projections.axial,
                ct_series_aggregate.projections.sagital,
                ct_series_aggregate.projections.coronal,
            )

        # Сохраняем Comments (если есть)
        for comment in ct_series_aggregate.comments:
            await self.connection.execute(
                """
                INSERT INTO comment (id, author, content, timestamp)
                VALUES ($1, $2, $3, $4)
                """,
                comment.id,
                comment.author,
                comment.content,
                comment.timestamp,
            )

    async def find_by_id(self, ct_series_id: str) -> Optional["CTSeriesAggregate"]:
        """Находит агрегат по ID."""
        # Загружаем CTSeries
        ct_series_record = await self.connection.fetchrow(
            """
            SELECT * FROM ct_series WHERE id = $1
            """,
            ct_series_id,
        )
        if not ct_series_record:
            return None

        ct_series = CTSeries(
            id=ct_series_record["id"],
            patient_id=ct_series_record["patient_id"],
            upload_date=ct_series_record["upload_date"],
            status=ct_series_record["status"],
        )

        # Загружаем Projections (если есть)
        projections_record = await self.connection.fetchrow(
            """
            SELECT * FROM projections WHERE id = $1
            """,
            ct_series_record["projections"],
        )
        projections = None
        if projections_record:
            projections = Projections(
                id=projections_record["id"],
                axial=projections_record["axial"],
                sagital=projections_record["sagital"],
                coronal=projections_record["coronal"],
            )

        # Загружаем Comments (если есть)
        comments_records = await self.connection.fetch(
            """
            SELECT * FROM comment WHERE id = $1
            """,
            ct_series_id,
        )
        comments = []
        for record in comments_records:
            comments.append(Comment(
                id=record["id"],
                author=record["author"],
                content=record["content"],
                timestamp=record["timestamp"],
            ))

        return CTSeriesAggregate(ct_series=ct_series, projections=projections, comments=comments)

    async def update(self, ct_series_aggregate: "CTSeriesAggregate") -> None:
        """Обновляет агрегат в БД."""
        # Обновляем CTSeries
        await self.connection.execute(
            """
            UPDATE ct_series
            SET patient_id = $2, upload_date = $3, status = $4
            WHERE id = $1
            """,
            ct_series_aggregate.ct_series.id,
            ct_series_aggregate.ct_series.patient_id,
            ct_series_aggregate.ct_series.upload_date,
            ct_series_aggregate.ct_series.status,
        )

        # Обновляем Projections (если есть)
        if ct_series_aggregate.projections:
            await self.connection.execute(
                """
                UPDATE projections
                SET axial = $2, sagital = $3, coronal = $4
                WHERE id = $1
                """,
                ct_series_aggregate.projections.id,
                ct_series_aggregate.projections.axial,
                ct_series_aggregate.projections.sagital,
                ct_series_aggregate.projections.coronal,
            )

        # Обновляем Comments (если есть)
        for comment in ct_series_aggregate.comments:
            await self.connection.execute(
                """
                UPDATE comment
                SET author = $2, content = $3, timestamp = $4
                WHERE id = $1
                """,
                comment.id,
                comment.author,
                comment.content,
                comment.timestamp,
            )
