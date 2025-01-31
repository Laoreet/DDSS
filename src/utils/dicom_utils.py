import os
import numpy as np
import pydicom
from pydicom.pixel_data_handlers.util import apply_voi_lut
import cv2
from PIL import Image
import io
import base64


IMAGE_SIZE = (128, 128)
BRAIN_HU = (22, 50)
BONES_HU = (220, 2000)
BLOOD_HU = (40, 100)


def get_dcm_serie(path_to_dcm_serie: str):
    ds_list = []
    dcm_files = os.listdir(path_to_dcm_serie)
    for file in dcm_files:
        buf_ds_file = pydicom.dcmread(
            os.path.join(path_to_dcm_serie, file), force=True
            )
        ds_list.append(buf_ds_file)

    if len(ds_list) > 0:
        if 'SamplesPerPixel' not in ds_list[0]:
            for el in ds_list:
                bits = el.Rows * el.Columns * el.BitsAllocated / 8
                float_pixs = len(el.PixelData) / (el.get('NumberOfFrames', 1) * bits)
                el.SamplesPerPixel = int(float_pixs)
        if 'PhotometricInterpretation' not in ds_list[0]:
            for el in ds_list:
                el.PhotometricInterpretation = 'MONOCHROME2'
        if 'RescaleSlope' not in ds_list[0]:
            for el in ds_list:
                el.RescaleSlope = 1

        try:
            firs_img_pos = ds_list[0].ImagePositionPatient[2]
            second_img_pos = ds_list[1].ImagePositionPatient[2]
            delta_pos = firs_img_pos - second_img_pos
            slice_thickness = np.abs(delta_pos)
        except Exception:
            delta_thick = ds_list[0].SliceLocation - ds_list[1].SliceLocation
            slice_thickness = np.abs(delta_thick)

        for el in ds_list:
            el.SliceThickness = slice_thickness

        return sorted(ds_list, key=lambda s: s.ImagePositionPatient[2])


def resize_and_voi_lut(dcm_file):
    if 'SamplesPerPixel' not in dcm_file:
        bits = dcm_file.Rows * dcm_file.Columns * dcm_file.BitsAllocated / 8
        pix_len = len(dcm_file.PixelData)
        dcm_file.SamplesPerPixel = pix_len / (dcm_file.get('NumberOfFrames', 1) * bits)
    if 'PhotometricInterpretation' not in dcm_file:
        dcm_file.PhotometricInterpretation = 'MONOCHROME2'
    buf_pixel_array = apply_voi_lut(dcm_file.pixel_array, dcm_file)
    resized_array = cv2.resize(buf_pixel_array,
                               IMAGE_SIZE,
                               interpolation=cv2.INTER_NEAREST)
    return resized_array


def get_pixels_hu(slices):
    image = np.stack([s.pixel_array for s in slices])
    image = image.astype(np.int16)

    for slice_number in range(len(slices)):
        intercept = slices[slice_number].RescaleIntercept
        slope = slices[slice_number].RescaleSlope

        if slope != 1:
            image[slice_number] = slope * image[slice_number].astype(np.float64)
            image[slice_number] = image[slice_number].astype(np.int16)

        image[slice_number] += np.int16(intercept)

    return np.array(image, dtype=np.int16)


def get_stacked_structures_from_dicom(dicom_list):
    resized_arr = [cv2.resize(x.pixel_array,
                              IMAGE_SIZE,
                              interpolation=cv2.INTER_NEAREST) for x in dicom_list]
    patient_pixels = np.array(resized_arr)

    brain = np.where((patient_pixels >= BRAIN_HU[0]) &
                     (patient_pixels <= BRAIN_HU[1]),
                     patient_pixels, 0)
    bones = np.where((patient_pixels >= BONES_HU[0]) &
                     (patient_pixels <= BONES_HU[1]),
                     patient_pixels, 0)
    blood = np.where((patient_pixels >= BLOOD_HU[0]) &
                     (patient_pixels <= BLOOD_HU[1]),
                     patient_pixels, 0)

    stacked_image = np.stack((brain, bones, blood), axis=0)

    return stacked_image


def preprocess_series(series):
    series = (series - np.min(series)) / (np.max(series) - np.min(series))
    return series.astype('float16')


def numpy_to_base64(image):
    img = Image.fromarray(image)
    img = img.convert('L')  # Преобразование в режим оттенков серого
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')


# Функция для вывода нескольких проекций (аксиальной, сагитальной, корональной)
def get_proections(ds_list):
    ds_list = sorted(ds_list, key=lambda s: s.ImagePositionPatient[2])

    # Создаем трехмерный массив
    img_shape = list(ds_list[0].pixel_array.shape)
    img_shape.append(len(ds_list))
    img3d = np.zeros(img_shape)
    # print(ds_list[0].pixel_array.shape)

    # Заполняем трехмерный массив нашими снимками (срезами),
    # увеличивая при этом их контрастность
    for i, s in enumerate(ds_list):
        img2d = apply_voi_lut(s.pixel_array, s)
        img3d[:, :, i] = img2d

    axial = numpy_to_base64(img3d[:, :, img_shape[2] // 2])
    sagital = numpy_to_base64(img3d[:, img_shape[1] // 2, :])
    coronal = numpy_to_base64(img3d[img_shape[0] // 2, :, :].T)

    return (axial, sagital, coronal)
