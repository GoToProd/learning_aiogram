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
from core.middlewares.apschedulermiddleware import ShedulerMiddleware
from aiogram.utils.chat_action import ChatActionMiddleware
from core.middlewares.example_chat_action_middleware import ExampleChatActionMiddleware

# import asyncpg
import psycopg_pool

from core.handlers import form
from core.utils.statesform import StepsForm

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from core.handlers import apsched
from datetime import datetime, timedelta

from aiogram.fsm.storage.redis import RedisStorage
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler_di import ContextSchedulerDecorator

from core.handlers import send_media

# фикс событий (актуально было на версию 3.00.4b)
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
    storage = RedisStorage.from_url("redis://localhost:6379/0")

    dp = Dispatcher(storage=storage)

    jobstores = {
        "default": RedisJobStore(
            jobs_key="dispatched_trips_jobs",
            run_times_key="dispatched_trips_running",
            host="localhost",
            db=2,
            port=6379,
        ),
    }

    # Работа с Sheduled модулем
    scheduler = ContextSchedulerDecorator(
        AsyncIOScheduler(timezone="Europe/Moscow", jobstores=jobstores)
    )
    scheduler.ctx.add_instance(bot, declared_class=Bot)
    scheduler.add_job(
        apsched.send_message_time,
        trigger="date",
        run_date=datetime.now() + timedelta(seconds=10),
        # kwargs={"bot": bot},
    )
    scheduler.add_job(
        apsched.send_message_cron,
        trigger="cron",
        hour=datetime.now().hour,
        minute=datetime.now().minute + 1,
        start_date=datetime.now(),
        # kwargs={"bot": bot},
    )
    scheduler.add_job(
        apsched.send_message_interval,
        trigger="interval",
        seconds=60,
        # kwargs={"bot": bot},
    )
    scheduler.start()

    # Управление запуском и остановкой бота
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    # Работа с медиа файлами
    dp.message.register(
        send_media.get_audio,
        Command(commands="audio"),
        flags={"chat_action": "upload_document"},
    )
    dp.message.register(
        send_media.get_document,
        Command(commands="document"),
        flags={"chat_action": "upload_document"},
    )
    dp.message.register(
        send_media.get_media_group,
        Command(commands="mediagroup"),
        flags={"chat_action": "upload_photo"},
    )
    dp.message.register(
        send_media.get_photo,
        Command(commands="photo"),
        flags={"chat_action": "upload_photo"},
    )
    dp.message.register(
        send_media.get_sticker,
        Command(commands="sticker"),
        flags={"chat_action": "choose_sticker"},
    )
    dp.message.register(
        send_media.get_video,
        Command(commands="video"),
        flags={"chat_action": "upload_video"},
    )
    dp.message.register(
        send_media.get_video_note,
        Command(commands="video_note"),
        flags={"chat_action": "upload_video_note"},
    )
    dp.message.register(
        send_media.get_voice,
        Command(commands="voice"),
        flags={"chat_action": "upload_voice"},
    )

    # Для работы с БД, счетчик сообщений и контроля часов работы
    dp.update.middleware.register(DbSession(pool_connect))
    dp.update.middleware.register(ShedulerMiddleware(scheduler))
    dp.message.middleware.register(CounterMiddleware())
    # dp.message.middleware.register(ChatActionMiddleware())
    dp.message.middleware.register(ExampleChatActionMiddleware())
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
