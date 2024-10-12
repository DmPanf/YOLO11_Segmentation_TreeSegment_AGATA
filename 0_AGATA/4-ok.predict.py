import cv2
import matplotlib.pyplot as plt
from ultralytics import YOLO
import numpy as np
import os

my_acc = 0.51  # Задаваемая точность для поиска

# Загрузка модели
model_path = '/content/drive/MyDrive/0.RTA/AGATA/agata1_segment_mask/runs/segment/0/weights/best.pt'
model = YOLO(model_path)

# Путь для сохранения результатов
output_dir = '/content/drive/MyDrive/0.RTA/AGATA/images/output'
os.makedirs(output_dir, exist_ok=True)

# Функция для выполнения сегментации с фильтрацией по точности и запасом 20% вокруг объекта
def segment_and_scale(image_path):
    # Загружаем изображение
    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Выполнение предсказания
    results = model.predict(source=image_rgb, imgsz=1280)

    # Фильтрация объектов с точностью (confidence) >= my_acc [0.95]
    filtered_boxes = []
    for r in results:
        for i, mask in enumerate(r.masks.xy):
            if r.boxes.conf[i] >= my_acc:
                # Масштабирование объекта с запасом 20% от рамки
                x, y, w, h = cv2.boundingRect(np.array(mask, dtype=np.int32))

                # Добавляем 20% к ширине и высоте рамки
                pad_w = int(w * 0.2)
                pad_h = int(h * 0.2)

                # Убедимся, что границы не выходят за пределы изображения
                x1 = max(0, x - pad_w)
                y1 = max(0, y - pad_h)
                x2 = min(image_rgb.shape[1], x + w + pad_w)
                y2 = min(image_rgb.shape[0], y + h + pad_h)

                # Вырезаем объект с запасом
                cropped_object = image_rgb[y1:y2, x1:x2]

                # Наносим зеленую рамку вокруг оригинального объекта
                cv2.rectangle(cropped_object, (pad_w, pad_h), (pad_w + w, pad_h + h), (0, 255, 0), 2)

                # Масштабируем объект
                scaled_object = cv2.resize(cropped_object, (cropped_object.shape[1] * 2, cropped_object.shape[0] * 2))

                # Сохраняем масштабированные объекты
                filtered_boxes.append((scaled_object, (x, y, w, h)))

    # Если не найдено объектов с точностью >= my_acc = 0.95
    if len(filtered_boxes) == 0:
        print(f"Нет объектов с точностью >= {my_acc}")
        return

    # Отображаем оригинальное изображение с рамками (но без нанесения рамок)
    plt.figure(figsize=(10, 10))
    plt.imshow(image_rgb)
    plt.title("Оригинальное изображение без рамок")
    plt.show()

    # Сохраняем оригинальное изображение
    original_output_path = os.path.join(output_dir, os.path.basename(image_path))
    cv2.imwrite(original_output_path, cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR))
    print(f"Оригинальное изображение сохранено: {original_output_path}")

    # Отображаем и сохраняем масштабированные объекты с запасом 20% и нанесенной зеленой рамкой
    for i, (obj, (x, y, w, h)) in enumerate(filtered_boxes):
        plt.figure(figsize=(10, 10))
        plt.imshow(obj)
        plt.title(f"Объект {i+1} (масштаб 2x с запасом 20%)")

        # Сохранение каждого увеличенного объекта
        scaled_output_path = os.path.join(output_dir, f"{os.path.splitext(os.path.basename(image_path))[0]}_object_{i+1}.jpg")
        cv2.imwrite(scaled_output_path, cv2.cvtColor(obj, cv2.COLOR_RGB2BGR))
        print(f"Масштабированный объект {i+1} сохранен: {scaled_output_path}")

        plt.show()

# Пример использования
image_path = '/content/drive/MyDrive/0.RTA/AGATA/images/ag43.jpg'
segment_and_scale(image_path)
