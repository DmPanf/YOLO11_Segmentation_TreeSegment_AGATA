# официальный образ Nginx
FROM nginx:stable-alpine

MAINTAINER "Dmitry <7292337@gmail.com>"
LABEL version="1.0"
LABEL description="Tree Segmentation
# Удаляем дефолтные файлы Nginx
RUN rm -rf /usr/share/nginx/html/*
# Копируем файлы сайта в контейнер
COPY . /usr/share/nginx/html
# Порт, на котором будет работать веб-сервер
EXPOSE 8080
