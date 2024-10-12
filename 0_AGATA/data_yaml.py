# Создание файла data.yaml для проекта
yaml_content = """
path: /content/drive/MyDrive/0.RTA/AGATA/Project  # путь к проекту
train: images/train  # относительный путь к тренировочным изображениям
val: images/val  # относительный путь к валидационным изображениям

nc: 1  # количество классов
names: ['DM']  # имя класса
"""

# Сохранение файла data.yaml
data_yaml_path = os.path.join(new_project_dir, 'data.yaml')
with open(data_yaml_path, 'w') as f:
    f.write(yaml_content)

print(f"Файл data.yaml успешно создан по пути: {data_yaml_path}")
