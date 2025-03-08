from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import torch
from utils.dicom_utils import get_dcm_serie, get_stacked_structures_from_dicom, preprocess_series, get_proections
from utils.model_utils import MedicalNet, get_attention_map_base64

app = FastAPI()

# Глобальные переменные
UPLOAD_FOLDER = "uploads"  # Путь к папке с загруженными файлами


# Модели для ответа
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


class ProcessRequest(BaseModel):
    id: str


class ProcessResponse(BaseModel):
    id: str
    status: str


# Загрузка модели
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
# model_dict = torch.load('models/final_checkpoint_good_preprocess.pth')
model = MedicalNet().to(device)
# try:
#     model.load_state_dict(model_dict['model_state_dict'])
# except Exception:
#     model = MedicalNet().to(device)
model.eval()


@app.post("/process", response_model=ProcessResponse)
async def process_files(request: ProcessRequest):
    study_id = request.id
    study_folder = os.path.join(UPLOAD_FOLDER, study_id)
    print(os.listdir(UPLOAD_FOLDER))
    if not os.path.exists(study_folder):
        raise HTTPException(status_code=404,
                            detail=f"Study with ID '{study_id}' not found.")

    # Обработка данных
    series = get_dcm_serie(study_folder)
    stacked_structures = get_stacked_structures_from_dicom(series)
    preprocessed_serie = preprocess_series(stacked_structures)
    input_ct = torch.tensor(preprocessed_serie, dtype=torch.float32).unsqueeze(0).to(device)

    with torch.no_grad():
        output = model(input_ct)
        print(output)

    # Здесь можно сохранить результаты обработки, если нужно
    return ProcessResponse(id=study_id, status="completed")


@app.get("/results/{id}", response_model=ResultResponse)
async def get_results(id: str):
    study_folder = os.path.join(UPLOAD_FOLDER, id)
    if not os.path.exists(study_folder):
        raise HTTPException(status_code=404,
                            detail=f"Study with ID '{id}' not found.")

    series = get_dcm_serie(study_folder)
    stacked_structures = get_stacked_structures_from_dicom(series)
    preprocessed_serie = preprocess_series(stacked_structures)
    input_ct = torch.tensor(preprocessed_serie, dtype=torch.float32).unsqueeze(0).to(device)

    with torch.no_grad():
        output = model(input_ct)

    hemorrhage_probability = output.item()

    return ResultResponse(id=id, status="completed", hemorrhage_probability=hemorrhage_probability)


@app.get("/projections/{id}", response_model=ProjectionsResponse)
async def get_projections(id: str):
    study_folder = os.path.join(UPLOAD_FOLDER, id)
    if not os.path.exists(study_folder):
        raise HTTPException(status_code=404, detail=f"Study with ID '{id}' not found.")

    series = get_dcm_serie(study_folder)
    axial_image, coronal_image, sagittal_image = get_proections(series)

    return ProjectionsResponse(axial=axial_image, coronal=coronal_image, sagittal=sagittal_image)


@app.get("/attention-maps/{id}", response_model=AttentionMapResponse)
async def get_attention_maps(id: str):
    study_folder = os.path.join(UPLOAD_FOLDER, id)
    if not os.path.exists(study_folder):
        raise HTTPException(status_code=404, detail=f"Study with ID '{id}' not found.")

    series = get_dcm_serie(study_folder)
    stacked_structures = get_stacked_structures_from_dicom(series)
    preprocessed_serie = preprocess_series(stacked_structures)
    input_ct = torch.tensor(preprocessed_serie, dtype=torch.float32).unsqueeze(0).to(device)

    attention_map_base64 = get_attention_map_base64(model, input_ct)

    return AttentionMapResponse(attention_map=attention_map_base64)
