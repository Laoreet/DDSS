from fastapi import FastAPI, HTTPException, Depends, UploadFile, File, Form
from pydantic import BaseModel
from typing import List
import asyncpg
from datetime import datetime
from infrastructure.ct_series_repository_sql import PostgreSQLCTSeriesRepository
from domain.aggregates.ct_series_aggregate import CTSeriesAggregate
from domain.entities.ct_series import CTSeries
from utils.base_uuid import BaseId
import os

app = FastAPI()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:123321a@localhost:5432/hse_ddss_brain")
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


async def get_db_connection():
    connection = await asyncpg.connect(DATABASE_URL)
    try:
        yield connection
    finally:
        await connection.close()


# Pydantic модель для входящих данных
class CTSeriesCreate(BaseModel):
    patient_id: str
    status: str
    # files: List[UploadFile]


class CTSeriesResponse(BaseModel):
    id: str
    patient_id: str
    upload_date: str
    status: str


@app.post("/ct_series/", response_model=CTSeriesResponse)
async def create_ct_series(patient_id: str = Form(...), status: str = Form(...), files: List[UploadFile] = File(...), db=Depends(get_db_connection)):
    ct_series_id = BaseId()  # Генерация нового ID
    ct_series_aggregate = CTSeriesAggregate(
        ct_series=CTSeries(
            id=ct_series_id,
            patient_id=patient_id,
            upload_date=datetime.now(),
            status=status,
        )
    )
    repository = PostgreSQLCTSeriesRepository(db)

    # Сохраняем сами наши файлы дикомовские
    study_folder = os.path.join(UPLOAD_FOLDER, str(ct_series_aggregate.ct_series.id))
    os.makedirs(study_folder, exist_ok=True)

    for file in files:
        if not file.filename.endswith(".dcm"):
            raise HTTPException(status_code=400,
                                detail={
                                    "error": "Bad Request",
                                    "message": "Invalid file format. Expected DICOM."
                                    })
        file_path = os.path.join(study_folder, file.filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())

    await repository.save(ct_series_aggregate)
    return CTSeriesResponse(id=str(ct_series_id), patient_id=patient_id, upload_date=str(ct_series_aggregate.ct_series.upload_date), status=ct_series_aggregate.ct_series.status)


@app.get("/ct_series/{ct_series_id}", response_model=CTSeriesResponse)
async def read_ct_series(ct_series_id: str, db=Depends(get_db_connection)):
    repository = PostgreSQLCTSeriesRepository(db)
    ct_series_aggregate = await repository.find_by_id(ct_series_id)
    if not ct_series_aggregate:
        raise HTTPException(status_code=404, detail="CT Series not found")
    return CTSeriesResponse(
        id=str(ct_series_aggregate.ct_series.id),
        patient_id=ct_series_aggregate.ct_series.patient_id,
        upload_date=str(ct_series_aggregate.ct_series.upload_date),
        status=ct_series_aggregate.ct_series.status,
    )


@app.put("/ct_series/{ct_series_id}", response_model=CTSeriesResponse)
async def update_ct_series(ct_series_id: str, ct_series: CTSeriesCreate, db=Depends(get_db_connection)):
    repository = PostgreSQLCTSeriesRepository(db)
    ct_series_aggregate = await repository.find_by_id(ct_series_id)
    if not ct_series_aggregate:
        raise HTTPException(status_code=404, detail="CT Series not found")

    ct_series_aggregate.ct_series.patient_id = ct_series.patient_id
    ct_series_aggregate.ct_series.status = ct_series.status
    await repository.update(ct_series_aggregate)

    return CTSeriesResponse(
        id=str(ct_series_aggregate.ct_series.id),
        patient_id=ct_series_aggregate.ct_series.patient_id,
        upload_date=str(ct_series_aggregate.ct_series.upload_date),
        status=ct_series_aggregate.ct_series.status,
    )


@app.delete("/ct_series/{ct_series_id}")
async def delete_ct_series(ct_series_id: str, db=Depends(get_db_connection)):
    repository = PostgreSQLCTSeriesRepository(db)
    ct_series_aggregate = await repository.find_by_id(ct_series_id)
    if not ct_series_aggregate:
        raise HTTPException(status_code=404, detail="CT Series not found")

    return {"detail": "CT Series deleted successfully"}
