import cv2
import matplotlib.pyplot as plt
from ultralytics import YOLO
import numpy as np

# Загрузка модели
model_path = '/content/drive/MyDrive/0.RTA/AGATA/agata1_segment_mask/runs/segment/0/weights/best.pt'
model = YOLO(model_path)

# Функция для выполнения сегментации с фильтрацией по точности
def segment_and_scale(image_path):
    # Загружаем изображение
    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Выполнение предсказания
    results = model.predict(source=image_rgb, imgsz=1280)

    # Фильтрация объектов с точностью (confidence) >= 0.95
    filtered_boxes = []
    for r in results:
        for i, mask in enumerate(r.masks.xy):
            if r.boxes.conf[i] >= 0.95:
                # Масштабирование объекта
                x, y, w, h = cv2.boundingRect(np.array(mask, dtype=np.int32))
                cropped_object = image_rgb[y:y+h, x:x+w]
                scaled_object = cv2.resize(cropped_object, (w * 2, h * 2))

                # Сохраняем масштабированные объекты для отображения
                filtered_boxes.append((scaled_object, (x, y, w, h)))

    # Если не найдено объектов с точностью >= 0.95
    if len(filtered_boxes) == 0:
        print("Нет объектов с точностью >= 0.95")
        return

    # Отображаем оригинальное изображение
    plt.figure(figsize=(10, 10))
    plt.subplot(1, len(filtered_boxes) + 1, 1)
    plt.imshow(image_rgb)
    plt.title("Оригинальное изображение")

    # Отображаем масштабированные объекты
    for i, (obj, (x, y, w, h)) in enumerate(filtered_boxes):
        plt.subplot(1, len(filtered_boxes) + 1, i + 2)
        plt.imshow(obj)
        plt.title(f"Объект {i+1} (масштаб 2x)")
    
    plt.show()

# Пример использования
image_path = '/content/drive/MyDrive/0.RTA/AGATA/images/ag31.jpg'
segment_and_scale(image_path)
