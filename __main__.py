import asyncio # импорт модуля для асинхронного запуска бота Подробнее https://habr.com/ru/companies/wunderfund/articles/700474/
import logging # импорт модуля для настройки логгирования, которое поможет в отладке Подробнее https://habr.com/ru/companies/wunderfund/articles/683880/

from aiogram import Bot, Dispatcher # основной модуль библиотеки aiogram, из которого мы импортируем классы Bot и Dispatcher Подробнее https://mastergroosha.github.io/aiogram-3-guide/quickstart/
from aiogram.fsm.storage.memory import MemoryStorage # хранилища данных для состояний пользователей

from config import TOKEN # импорт токена из файла конфигурации - предварительно нужно записать токен в этот файл как значение переменной TOKEN

from handlers import router # обработчики команд бота

async def main(): # главная процедура
    bot = Bot(token=TOKEN) # создание объекта бота с нашим токеном
    dp = Dispatcher(storage=MemoryStorage()) # создание объекта диспетчера, параметр storage=MemoryStorage() говорит о том, что все данные бота будут стёрты при перезапуске
    dp.include_router(router) # подключение к нашему диспетчеру всех обработчиков, которые используют router из модуля handlers
    await bot.delete_webhook(drop_pending_updates=True) # удаление всех обновлений, которые произошли после последнего завершения работы бота
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types()) # запуск прослушивания бота


if __name__ == "__main__": # выполняем при запуске именно этого файла
    logging.basicConfig(level=logging.INFO) # запуск логгирования
    asyncio.run(main()) # асинхронный запуск главной процедуры
