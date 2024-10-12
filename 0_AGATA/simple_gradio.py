# 
# !pip install -qqq gradio

import gradio as gr
from ultralytics import YOLO
import cv2

# Загрузка модели сегментации
model_path = '/content/drive/MyDrive/0.RTA/AGATA/agata1_segment_mask/runs/segment/0/weights/best.pt'
model = YOLO(model_path)  # Загрузка обученной модели

# Функция для выполнения сегментации
def segment_image(image):
    # Выполнение предсказания с использованием модели YOLO
    results = model.predict(image, imgsz=1280, conf=0.25)
    
    # Получаем аннотированное изображение с наложенными масками
    result_image = results[0].plot()  # Рисуем результат
    
    return result_image

# Интерфейс Gradio
interface = gr.Interface(
    fn=segment_image,  # Функция сегментации
    inputs=gr.Image(type="pil"),  # Входное изображение
    outputs=gr.Image(type="pil"),  # Выходное изображение с сегментацией
    title="Сегментация с YOLO11",  # Заголовок приложения
    description="Загрузите изображение, чтобы выполнить сегментацию",  # Описание
)

# Запуск приложения
interface.launch(debug=True)
