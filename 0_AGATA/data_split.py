import os
import shutil
import random

# Пути к папкам с изображениями и метками
project_dir = '/content/drive/MyDrive/0.RTA/AGATA/Project'
images_dir = os.path.join(project_dir, 'images/train')
labels_dir = os.path.join(project_dir, 'labels/train')

# Папки для перемещенных файлов
train_images_dir = os.path.join(project_dir, 'images/train')
val_images_dir = os.path.join(project_dir, 'images/val')
train_labels_dir = os.path.join(project_dir, 'labels/train')
val_labels_dir = os.path.join(project_dir, 'labels/val')

# Создание папок для train и val, если они не существуют
os.makedirs(train_images_dir, exist_ok=True)
os.makedirs(val_images_dir, exist_ok=True)
os.makedirs(train_labels_dir, exist_ok=True)
os.makedirs(val_labels_dir, exist_ok=True)

# Получение списка всех изображений
all_images = os.listdir(images_dir)

# Сортировка файлов изображений (без расширения) для разделения на train и val
all_files = [os.path.splitext(f)[0] for f in all_images]

# Перемешиваем файлы
random.shuffle(all_files)

# Разделение на 75% для train и 25% для val
train_size = int(0.75 * len(all_files))
train_files = all_files[:train_size]
val_files = all_files[train_size:]

# Функция для перемещения файлов
def move_files(files_list, src_images_dir, src_labels_dir, dst_images_dir, dst_labels_dir):
    for file_name in files_list:
        # Перемещение изображения
        src_image_path = os.path.join(src_images_dir, file_name + '.jpg')
        dst_image_path = os.path.join(dst_images_dir, file_name + '.jpg')
        if os.path.exists(src_image_path):
            shutil.move(src_image_path, dst_image_path)

        # Перемещение файла меток
        src_label_path = os.path.join(src_labels_dir, file_name + '.txt')
        dst_label_path = os.path.join(dst_labels_dir, file_name + '.txt')
        if os.path.exists(src_label_path):
            shutil.move(src_label_path, dst_label_path)

# Перемещение файлов в train
move_files(train_files, images_dir, labels_dir, train_images_dir, train_labels_dir)

# Перемещение файлов в val
move_files(val_files, images_dir, labels_dir, val_images_dir, val_labels_dir)

print(f"Файлы успешно разделены. В train: {len(train_files)}, в val: {len(val_files)}.")
