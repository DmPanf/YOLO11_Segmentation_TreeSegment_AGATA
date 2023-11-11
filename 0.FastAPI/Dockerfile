# Dockerfile
FROM python:3.9

MAINTAINER "Dmitry <7292337@gmail.com>"
LABEL version="1.0"
LABEL description="Tree Segmentation FastAPI + Telegram Bot"

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8001

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8001"]
#CMD ["uvicorn", "app:app", "--host", "localhost", "--port", "8001"]
