# Используйте официальный образ Python
#FROM python:3.8-slim-buster
FROM python:3.9

# Установите рабочую директорию
WORKDIR /app

# Копируйте файлы с зависимостями и установите их
COPY requirements.txt .

# Установка библиотеки libGL
RUN apt-get update && apt-get install -y libgl1-mesa-glx

RUN pip install --no-cache-dir -r requirements.txt --default-timeout=100

# Копируйте остальные файлы приложения
COPY . .

# Откройте порт для приложения
EXPOSE 5000

# Запустите приложение
CMD ["python", "app.py"]
