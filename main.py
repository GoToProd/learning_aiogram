import os
import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.client.bot import DefaultBotProperties
from aiogram.filters import Command, CommandStart
from core.filters.iscontact import IsTrueContact
from core.handlers.basic import (
    get_start,
    get_photo,
    get_hello,
    get_location,
    get_inline,
)
from core.handlers.contact import get_true_contact, get_false_contact
from core.handlers.callback import select_macbook
from dotenv.main import load_dotenv
from core.utils.commands import set_commands
from core.utils.callbackdata import MacInfo
from core.handlers.pay import (
    order,
    pre_checkout_query,
    successful_payment,
    shipping_check,
)
from core.middlewares.countermiddleware import CounterMiddleware

# from core.middlewares.officehourse import OfficeHourseMiddleware
from core.middlewares.dbmiddleware import DbSession

# import asyncpg
import psycopg_pool

from core.handlers import form
from core.utils.statesform import StepsForm


# asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


load_dotenv()
ADMIN_ID = os.getenv("ADMIN_ID")
TOKEN_API = os.getenv("TOKEN_API")


async def start_bot(bot: Bot):
    await set_commands(bot)
    await bot.send_message(ADMIN_ID, text="Бот запущен!")


async def stop_bot(bot: Bot):
    await bot.send_message(ADMIN_ID, text="Бот остановлен")


# async def create_pool():
# return await asyncpg.create_pool(
#     user="postgres",
#     password="postgres",
#     database="users",
#     host="127.0.0.1",
#     port=5432,
#     command_timeout=60,
# )
def create_pool():
    return psycopg_pool.AsyncConnectionPool(
        f"host=127.0.0.1 port=5432 dbname=users user=postgres password=postgres connect_timeout=60"
    )


async def start():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - [%(levelname)s] - [%(name)s] - [%(filename)s - "
        "(%(filename)s).%(funcName)s(%(lineno)d - %(message)s",
    )

    bot = Bot(TOKEN_API, default=DefaultBotProperties(parse_mode="HTML"))
    # pool_connect = await create_pool()
    pool_connect = create_pool()

    dp = Dispatcher()

    # Управление запуском и остановкой бота
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    # Для работы с БД, счетчик сообщений и контроля часов работы
    dp.update.middleware.register(DbSession(pool_connect))
    dp.message.middleware.register(CounterMiddleware())
    # dp.message.middleware.register(OfficeHourseMiddleware())

    # Для инлайн клавиатуры
    dp.message.register(get_inline, Command(commands="inline"))
    dp.callback_query.register(
        select_macbook, MacInfo.filter()
    )  # как вариант для фильтрации (F.model == "pro"))

    # Для работы с состоянием (опрос)
    dp.message.register(form.get_form, Command(commands="form"))
    dp.message.register(form.get_name, StepsForm.GET_NAME)
    dp.message.register(form.get_last_name, StepsForm.GET_LAST_NAME)
    dp.message.register(form.get_age, StepsForm.GET_AGE)

    # Для оформления заказа
    dp.message.register(order, Command(commands="pay"))
    dp.shipping_query.register(shipping_check)
    dp.pre_checkout_query.register(pre_checkout_query)
    dp.message.register(successful_payment, F.successful_payment)

    # Для получения обычных данных через кнопки
    dp.message.register(get_location, F.location)
    dp.message.register(get_hello, F.text == "Привет")
    dp.message.register(get_true_contact, F.contact, IsTrueContact())
    dp.message.register(get_false_contact, F.contact)
    dp.message.register(get_photo, F.photo)
    dp.message.register(get_start, Command(commands=["start", "run"]))
    # dp.message.register(get_start, CommandStart)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(start())
