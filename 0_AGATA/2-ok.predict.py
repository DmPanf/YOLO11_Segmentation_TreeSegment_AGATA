import cv2
import matplotlib.pyplot as plt
from ultralytics import YOLO
import numpy as np
import os

# Загрузка модели
model_path = '/content/drive/MyDrive/0.RTA/AGATA/agata1_segment_mask/runs/segment/0/weights/best.pt'
model = YOLO(model_path)

# Путь для сохранения результатов
output_dir = '/content/drive/MyDrive/0.RTA/AGATA/images/output'
os.makedirs(output_dir, exist_ok=True)

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

                # Сохраняем масштабированные объекты и координаты для рамки
                filtered_boxes.append((scaled_object, (x, y, w, h)))

                # Рисуем рамку на оригинальном изображении
                cv2.rectangle(image_rgb, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Если не найдено объектов с точностью >= 0.95
    if len(filtered_boxes) == 0:
        print("Нет объектов с точностью >= 0.95")
        return

    # Сохраняем оригинальное изображение с рамками
    original_output_path = os.path.join(output_dir, os.path.basename(image_path))
    cv2.imwrite(original_output_path, cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR))
    print(f"Оригинальное изображение с рамками сохранено: {original_output_path}")

    # Отображаем и сохраняем масштабированные объекты
    for i, (obj, (x, y, w, h)) in enumerate(filtered_boxes):
        plt.figure(figsize=(10, 10))
        plt.imshow(obj)
        plt.title(f"Объект {i+1} (масштаб 2x)")
        
        # Сохранение каждого увеличенного объекта
        scaled_output_path = os.path.join(output_dir, f"{os.path.splitext(os.path.basename(image_path))[0]}_object_{i+1}.jpg")
        cv2.imwrite(scaled_output_path, cv2.cvtColor(obj, cv2.COLOR_RGB2BGR))
        print(f"Масштабированный объект {i+1} сохранен: {scaled_output_path}")
        
        plt.show()

# Пример использования
image_path = '/content/drive/MyDrive/0.RTA/AGATA/images/ag31.jpg'
segment_and_scale(image_path)
