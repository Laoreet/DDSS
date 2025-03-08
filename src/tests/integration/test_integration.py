import pytest
import httpx
import os

# Базовые URL для сервисов
SERVICE1_URL = "http://localhost:8000"
SERVICE2_URL = "http://localhost:8001"


test_dicom_files = ['tests/integration/slice_0.dcm', 'tests/integration/slice_1.dcm']

@pytest.mark.asyncio
async def test_upload_and_process():
    timeout = httpx.Timeout(20.0)
    # Загружаем файл в service1
    async with httpx.AsyncClient(timeout=timeout) as client:
        with open(test_dicom_files[0], "rb") as file1:
            with open(test_dicom_files[1], "rb") as file2:
                response = await client.post(
                    f"{SERVICE1_URL}/upload",
                    files=[("files", file1), ('files', file2)]
                )
        assert response.status_code == 200
        study_id = response.json()["id"]
        # Проверяем, что service2 обработал файл
        response = await client.get(f"{SERVICE2_URL}/results/{study_id}")
        assert response.status_code == 200
        assert response.json()["status"] == "completed"

@pytest.mark.asyncio
async def test_missing_results():
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{SERVICE2_URL}/results/missing",
        )
        assert response.status_code == 404
        assert response.json()["detail"] == "Study with ID 'missing' not found."

@pytest.mark.asyncio
async def test_missing_projections():
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{SERVICE2_URL}/projections/missing",
        )
        assert response.status_code == 404
        assert response.json()["detail"] == "Study with ID 'missing' not found."


@pytest.mark.asyncio
async def test_missing_attention_maps():
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{SERVICE2_URL}/attention-maps/missing",
        )
        assert response.status_code == 404
        assert response.json()["detail"] == "Study with ID 'missing' not found."
