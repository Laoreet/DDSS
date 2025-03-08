from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
from typing import List
import os
import uuid
import httpx

app = FastAPI()

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# URL сервиса 2 (можно задать через переменные окружения)
SERVICE2_URL = os.getenv("SERVICE2_URL", "http://service2:8001")


# Модели для ответа
class UploadResponse(BaseModel):
    id: str
    status: str


class DeleteResponse(BaseModel):
    status: str


class UpdateResponse(BaseModel):
    id: str
    comment: str


@app.post("/upload", response_model=UploadResponse)
async def upload_files(files: List[UploadFile] = File(...)):
    if not files:
        raise HTTPException(status_code=400,
                            detail={"error": "Bad Request", "message": "No files provided."})

    study_id = str(uuid.uuid4())
    study_folder = os.path.join(UPLOAD_FOLDER, study_id)
    os.makedirs(study_folder, exist_ok=True)

    for file in files:
        if not file.filename.endswith(".dcm"):
            raise HTTPException(status_code=400,
                                detail={"error": "Bad Request", "message": "Invalid file format. Expected DICOM."})
        file_path = os.path.join(study_folder, file.filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{SERVICE2_URL}/process",
                json={"id": study_id}
            )
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=500, detail=f"Error processing files: {str(e)}")

    return UploadResponse(id=study_id, status="processing")


@app.delete("/results/{id}", response_model=DeleteResponse)
async def delete_results(id: str):
    study_folder = os.path.join(UPLOAD_FOLDER, id)
    if not os.path.exists(study_folder):
        raise HTTPException(status_code=404, detail=f"Study with ID '{id}' not found.")
    for file in os.listdir(study_folder):
        os.remove(os.path.join(study_folder, file))
    os.rmdir(study_folder)
    return DeleteResponse(status="deleted")


@app.put("/results/{id}", response_model=UpdateResponse)
async def update_results(id: str, comment: str):
    study_folder = os.path.join(UPLOAD_FOLDER, id)
    if not os.path.exists(study_folder):
        raise HTTPException(status_code=404, detail=f"Study with ID '{id}' not found.")
    metadata_file = os.path.join(study_folder, "metadata.txt")
    with open(metadata_file, "w") as f:
        f.write(comment)

    return UpdateResponse(id=id, comment=comment)
