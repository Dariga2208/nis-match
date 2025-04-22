import time
import logging
import asyncio
import os
from aiohttp import web  # 👈

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from config import BOT_TOKEN
from handlers import questionnaire, view_profiles

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация бота
bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher(storage=MemoryStorage())

dp.include_router(questionnaire.router)
dp.include_router(view_profiles.router)

# 👇 Асинхронная функция запуска бота
async def start_bot():
    try:
        logger.info("Бот запускается...")
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Произошла ошибка: {e}")
        logger.info("Попробую перезапустить через 1 секунду...")
        time.sleep(1)
        await start_bot()

# 👇 AIOHTTP web server setup
async def on_startup(app):
    asyncio.create_task(start_bot())

# Настройка веб-сервера aiohttp
app = web.Application()
app.on_startup.append(on_startup)

# 👇 Запуск HTTP сервера на порту, предоставленном Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))  # Используем PORT, который предоставляется Render
    web.run_app(app, port=port)
