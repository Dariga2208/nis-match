import time
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from config import BOT_TOKEN
from handlers import questionnaire, view_profiles

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация бота с токеном
bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher(storage=MemoryStorage())

# Асинхронная функция для старта поллинга с обработкой ошибок
async def start_polling():
    try:
        # Включаем роутеры для работы с обработчиками
        dp.include_router(questionnaire.router)
        dp.include_router(view_profiles.router)

        # Запускаем процесс поллинга
        logger.info("Бот запускается...")
        await dp.start_polling(bot)

    except Exception as e:
        logger.error(f"Произошла ошибка: {e}")
        logger.info("Попробую перезапустить через 1 секунду...")
        time.sleep(1)  # Задержка перед повторной попыткой
        await start_polling()

# Запуск бота
if __name__ == "__main__":
    import asyncio
    asyncio.run(start_polling())
