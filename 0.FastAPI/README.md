## FastAPI Server DOCS & REDOC
<p>
<img src="https://raw.githubusercontent.com/terrainternship/rostelecom_tree_segmentation/dev/command/Dmitry_Panfilov/images/fastapi-1.jpg" width="38%">
<img src="https://raw.githubusercontent.com/terrainternship/rostelecom_tree_segmentation/dev/command/Dmitry_Panfilov/images/fastapi-2.jpg" width="55%">
</p>

## Web-Client (в связке с FastAPI + Telegram-Bot в Docker)

![image](https://github.com/terrainternship/rostelecom_tree_segmentation/assets/99917230/b8ffa276-0308-4b1a-97e1-639f055816df)


---

Для использования вашей модели в контейнере Docker вам нужно сделать следующее:

1. Убедитесь, что модель и метки классов доступны в контейнере Docker. Вы можете либо копировать их в Dockerfile, либо использовать тома Docker для их предоставления.

2. Установите зависимости, необходимые для вашей модели, в контейнере Docker. В вашем случае это `tensorflow`.

3. Импортируйте и используйте вашу модель в вашем коде.

Вот пример, как можно обновить ваш Dockerfile и docker-compose.yml:

Dockerfile:

```Dockerfile
# Set base image
FROM python:3.9

MAINTAINER "Dmitry <7292337@gmail.com>"
LABEL version="1.0"
LABEL description="Tree Segmentation FastAPI + Telegram Bot"

# Set the working directory
WORKDIR /app

# Copying the dependencies file
COPY requirements.txt .

# Installing dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copying files into working directory
COPY . .

# Copying your model and labels into the Docker image
COPY path/to/your/model /app/model
COPY path/to/your/labels /app/labels

# Port to be listening at runtime
EXPOSE 8001

# Running the application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8001"]
```

docker-compose.yml:

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8001:8001"
    volumes:
      - .:/app
    command: ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]
    networks:
      - my_network
    restart: unless-stopped

  bot:
    build: .
    volumes:
      - .:/app
    command: ["python", "bot.py"]
    networks:
      - my_network
    env_file:
      - .env
    restart: unless-stopped

networks:
  my_network:
```

Обновите файл `requirements.txt`:

```
fastapi
uvicorn
opencv-python-headless
Pillow
python-multipart
aiofiles
aiogram
aiohttp
python-dotenv
requests
tensorflow
```

Теперь вы должны импортировать и использовать свою модель в вашем коде. Пример:

```python
from pilot_model import pilot_model

# Load your model
model = pilot_model()

# Use your model
result = model.predict(data)
```

Убедитесь, что вы обновили пути к вашей модели и меткам классов в `pilot_model.py` на соответствующие пути в контейнере Docker.
