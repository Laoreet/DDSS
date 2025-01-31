from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List
import os
import uuid
import torch
from utils.dicom_utils import get_proections, get_dcm_serie
from utils.dicom_utils import get_stacked_structures_from_dicom, preprocess_series
from utils.model_utils import MedicalNet, get_attention_map_base64

app = FastAPI()

# Глобальные переменные
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# Модель для ответа
class UploadResponse(BaseModel):
    id: str
    status: str


class ResultResponse(BaseModel):
    id: str
    status: str
    hemorrhage_probability: float


class ProjectionsResponse(BaseModel):
    axial: str
    coronal: str
    sagittal: str


class AttentionMapResponse(BaseModel):
    attention_map: str


class DeleteResponse(BaseModel):
    status: str


class UpdateResponse(BaseModel):
    id: str
    comment: str


device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
# Загрузка модели
model = MedicalNet().to(device)
try:
    model_dict = torch.load(r'models\final_checkpoint_good_preprocess.pth')
    model.load_state_dict(model_dict['model_state_dict'])
except Exception:
    model = MedicalNet().to(device)
# model.eval()


@app.post("/upload", response_model=UploadResponse)
async def upload_files(files: List[UploadFile] = File(...)):
    if not files:
        raise HTTPException(status_code=400, detail={"error": "Bad Request",
                                                     "message": "No files provided."})

    study_id = str(uuid.uuid4())
    study_folder = os.path.join(UPLOAD_FOLDER, study_id)
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

    return UploadResponse(id=study_id, status="processing")


@app.get("/results/{id}", response_model=ResultResponse)
async def get_results(id: str):
    study_folder = os.path.join(UPLOAD_FOLDER, id)
    if not os.path.exists(study_folder):
        raise HTTPException(status_code=404, detail=f"Study with ID '{id}' not found.")

    series = get_dcm_serie(study_folder)
    stacked_structures = get_stacked_structures_from_dicom(series)
    preprocessed_serie = preprocess_series(stacked_structures)
    input_ct = torch.tensor(preprocessed_serie, dtype=torch.float32)
    input_ct = input_ct.unsqueeze(0).to(device)

    with torch.no_grad():
        output = model(input_ct)

    hemorrhage_probability = output.item()

    return ResultResponse(id=id, status="completed",
                          hemorrhage_probability=hemorrhage_probability)


@app.get("/projections/{id}", response_model=ProjectionsResponse)
async def get_projections(id: str):
    study_folder = os.path.join(UPLOAD_FOLDER, id)
    if not os.path.exists(study_folder):
        raise HTTPException(status_code=404, detail=f"Study with ID '{id}' not found.")

    series = get_dcm_serie(study_folder)
    axial_image, coronal_image, sagittal_image = get_proections(series)

    return ProjectionsResponse(axial=axial_image,
                               coronal=coronal_image, sagittal=sagittal_image)


@app.get("/attention-maps/{id}", response_model=AttentionMapResponse)
async def get_attention_maps(id: str):
    study_folder = os.path.join(UPLOAD_FOLDER, id)
    if not os.path.exists(study_folder):
        raise HTTPException(status_code=404, detail=f"Study with ID '{id}' not found.")
    series = get_dcm_serie(study_folder)
    stacked_structures = get_stacked_structures_from_dicom(series)
    preprocessed_serie = preprocess_series(stacked_structures)
    input_ct = torch.tensor(preprocessed_serie, dtype=torch.float32)
    input_ct = input_ct.unsqueeze(0).to(device)
    attention_map_base64 = get_attention_map_base64(model, input_ct)

    return AttentionMapResponse(attention_map=attention_map_base64)


@app.delete("/results/{id}", response_model=DeleteResponse)
async def delete_results(id: str):
    study_folder = os.path.join(UPLOAD_FOLDER, id)
    if not os.path.exists(study_folder):
        raise HTTPException(status_code=404, detail=f"Study with ID '{id}' not found.")

    os.rmdir(study_folder)
    return DeleteResponse(status="deleted")


@app.put("/results/{id}", response_model=UpdateResponse)
async def update_results(id: str, comment: str):
    study_folder = os.path.join(UPLOAD_FOLDER, id)
    if not os.path.exists(study_folder):
        raise HTTPException(status_code=404, detail=f"Study with ID '{id}' not found.")

    # Обновление метаданных (например, добавление комментария врача)
    # Пока что пусть будет в формате .txt
    metadata_file = os.path.join(study_folder, "metadata.txt")
    with open(metadata_file, "w") as f:
        f.write(comment)

    return UpdateResponse(id=id, comment=comment)


# Обработчики ошибок
@app.exception_handler(400)
async def bad_request_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=400,
        content={"error": "Bad Request", "message": exc.detail},
    )


@app.exception_handler(404)
async def not_found_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=404,
        content={"error": "Not Found", "message": exc.detail},
    )


@app.exception_handler(500)
async def internal_server_error_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=500,
        content={"error": "Internal Server Error",
                 "message": "An unexpected error occurred. Please try again later."},
    )
