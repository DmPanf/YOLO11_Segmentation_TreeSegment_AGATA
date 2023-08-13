import logging
import requests
import asyncio
from io import BytesIO

USER_API_TOKEN = '' # !!! добавить свои данные
USER_ID = ''        # !!! добавить свои данные
#FastAPI_URL = 'http://api-serv.ru:8001/process_image'
FastAPI_URL = 'http://51.250.26.141:8001/process_image'

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ParseMode
from aiogram.utils import executor

API_TOKEN = USER_API_TOKEN

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)

dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

@dp.message_handler(content_types=types.ContentType.PHOTO)
async def process_image(message: types.Message):
    # Получение файла изображения
    file_id = message.photo[-1].file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path

    # Загрузка изображения
    image_data = await bot.download_file(file_path)

    # Отправка изображения на сервер
    url = FastAPI_URL  # адрес сервера FastAPI
    response = requests.post(url, files={"image": ("input_image.png", image_data, "image/png")})

    if response.status_code == 200:
        # Получение обработанного изображения и отправка его обратно пользователю
        output_image_data = BytesIO(response.content)
        output_image_data.seek(0)
        await message.reply_photo(photo=output_image_data, caption="Обработанное изображение")

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    text = "Привет! Я бот для обработки изображений. Отправьте мне фотографию, и я верну вам обработанное изображение."
    await message.reply(text, parse_mode=ParseMode.MARKDOWN)

async def main():
    while True:
        try:
            await bot.send_message(chat_id=USER_ID, text="Бот запущен")
            await dp.start_polling()
        except Exception as e:
            logging.exception("Ошибка во время выполнения бота")
            await bot.send_message(chat_id=USER_ID, text="Бот остановлен")
            await asyncio.sleep(5)

if __name__ == '__main__':
    asyncio.run(main())
