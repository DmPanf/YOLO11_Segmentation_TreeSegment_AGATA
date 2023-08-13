from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from io import BytesIO
from PIL import Image
import numpy as np
import cv2
import tempfile

app = FastAPI()

# Добавляем middleware для CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Функция для обработки изображения
def pilot_model(input_image):
    # Преобразуем изображение в массив numpy
    image_array = np.array(input_image)
    # Преобразуем массив в изображение OpenCV
    image = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    dark_green_lower = (25, 52, 72)
    dark_green_upper = (102, 255, 255)
    light_green_lower = (35, 50, 50)
    light_green_upper = (85, 255, 255)
    dark_green_mask = cv2.inRange(hsv, dark_green_lower, dark_green_upper)
    light_green_mask = cv2.inRange(hsv, light_green_lower, light_green_upper)
    mask = cv2.bitwise_or(dark_green_mask, light_green_mask)
    result = cv2.bitwise_and(image, image, mask=mask)
    _, thresholded = cv2.threshold(mask, 1, 255, cv2.THRESH_BINARY)
    result[thresholded == 255] = (0, 255, 0)
    result[thresholded == 0] = (0, 0, 0)
    # Преобразуем изображение OpenCV в массив numpy
    result_array = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
    return result_array

# Обработка изображения
@app.post("/process_image")
async def process_image(image: UploadFile = File(...)):
    # Загрузка изображения из запроса
    image_data = await image.read()
    pil_image = Image.open(BytesIO(image_data))

    # Обработка изображения с помощью функции pilot_model
    result = pilot_model(pil_image)

    # Сохранение результата во временный файл
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
        cv2.imwrite(temp_file.name, result)

        # Отправка результата обратно клиенту
        return FileResponse(temp_file.name, media_type="image/png", headers={"Content-Disposition": f"attachment; filename={image.filename}_processed.png"})
