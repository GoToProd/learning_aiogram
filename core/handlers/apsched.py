import os
from dotenv.main import load_dotenv
from aiogram import Bot

load_dotenv()
ADMIN_ID = os.getenv("ADMIN_ID")


async def send_message_time(bot: Bot):
    await bot.send_message(
        ADMIN_ID,
        f"Это сообщение будет отправлено через несколько секунд после старта бота",
    )


async def send_message_cron(bot: Bot):
    await bot.send_message(
        ADMIN_ID, f"Это сообщение будет отправлено в опрделенное время каждый день"
    )


async def send_message_interval(bot: Bot):
    await bot.send_message(
        ADMIN_ID, f"Это сообщение будет отправлено через 1 минуту времени постоянно"
    )


async def send_message_middleware(bot: Bot, chat_id: int):
    await bot.send_message(
        chat_id,
        f"Это сообщение отправлено с помощью сформированной через middleware задачи",
    )
