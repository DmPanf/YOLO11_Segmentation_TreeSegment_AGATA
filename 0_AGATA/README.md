##


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
