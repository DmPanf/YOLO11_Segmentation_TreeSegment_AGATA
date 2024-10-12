## Google Colab

<code>
!nvidia-smi
    
# Подключение Google Drive
from google.colab import drive
drive.mount('/content/drive')

import os
home = '/content/drive/MyDrive/0.RTA/AGATA'
os.chdir(home)
os.listdir()
</code>code>

## YOLO11 predict

<code>
import os
home = '/content/drive/MyDrive/0.RTA/AGATA'
os.chdir(home)
os.listdir()

!pip install -qqq ultralytics

# Test YOLO11
# wget https://github.com/ultralytics/assets/releases/download/v8.3.0/yolo11x-seg.pt
my_img = '/content/drive/MyDrive/0.RTA/AGATA/images/14.jpg'
!yolo task=segment mode=predict model=yolo11x-seg.pt imgsz=640 conf=0.25 source=$my_img project=0

</code>


## COCO convert to YOLO

<code>
from ultralytics.data.converter import convert_coco

convert_coco(labels_dir="/content/drive/MyDrive/0.RTA/AGATA/agata1_coco/annotations", use_segments=True)
</code>


## COCO files COPY

<code>
import os
import shutil

# Пути к существующим данным и новой папке проекта
source_images_dir = '/content/drive/MyDrive/0.RTA/AGATA/agata1_coco/images'
source_labels_dir = '/content/drive/MyDrive/0.RTA/AGATA/agata1_segment_mask/coco_converted/labels/default'
new_project_dir = '/content/drive/MyDrive/0.RTA/AGATA/Project'

# Создание новой папки для проекта
os.makedirs(os.path.join(new_project_dir, 'images/train'), exist_ok=True)
os.makedirs(os.path.join(new_project_dir, 'images/val'), exist_ok=True)
os.makedirs(os.path.join(new_project_dir, 'labels/train'), exist_ok=True)
os.makedirs(os.path.join(new_project_dir, 'labels/val'), exist_ok=True)

# Копирование изображений
for image in os.listdir(source_images_dir):
    src_image_path = os.path.join(source_images_dir, image)
    dst_image_path = os.path.join(new_project_dir, 'images/train', image)
    shutil.copy(src_image_path, dst_image_path)

# Копирование файлов меток
for label in os.listdir(source_labels_dir):
    src_label_path = os.path.join(source_labels_dir, label)
    dst_label_path = os.path.join(new_project_dir, 'labels/train', label)
    shutil.copy(src_label_path, dst_label_path)

print("Копирование изображений и меток завершено.")
</code>

---

## Files Check

<code>
# Настройка локали на UTF-8
!export LC_ALL=C.UTF-8
!export LANG=C.UTF-8

# Проверка наличия файлов в папках
!ls /content/drive/MyDrive/0.RTA/AGATA/Project/labels/train
!pwd
!ls /content/drive/MyDrive/0.RTA/AGATA/Project/labels/val
</code>

---

## YOLO11 Train

<code>
from ultralytics import YOLO

# Загрузка модели сегментации
model = YOLO('yolo11l-seg.pt')  # модель сегментации

# Запуск обучения
model.train(
    data='/content/drive/MyDrive/0.RTA/AGATA/Project/data.yaml',  
    epochs=700,  # Количество эпох 
    imgsz=1280,  # Размер изображений
    batch=8,   # Размер батча
    name='1'   # Имя эксперимента
)

</code>
