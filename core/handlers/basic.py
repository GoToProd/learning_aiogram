import os
import json
from aiogram import Bot, F, Router
from aiogram.types import Message
from core.keyboards.reply import (
    reply_keyboard,
    local_tel_pol_keyboard,
    get_reply_keyboard,
)
from core.keyboards.inline import select_macbook, get_inline_keyboard


router = Router()
file_path = os.path.abspath("answer.json")


async def get_start(message: Message, bot: Bot):
    await message.answer(
        f"<s>Привет {message.from_user.username}, {message.from_user.first_name}</s>",
        reply_markup=get_reply_keyboard(),
    )


async def get_inline(message: Message, bot: Bot):
    await message.answer(
        f"Привет, {message.from_user.first_name}. Показываю инлайн кнопки",
        reply_markup=get_inline_keyboard(),
    )


async def get_location(message: Message, bot: Bot):
    await message.answer(
        f"Ты отправил локацию\r\a",
        f"{message.location.latitude} \r\n {message.location.longitude}",
    )


@router.message(F.photo)
async def get_photo(message: Message, bot: Bot):
    await message.answer(f"Отлично, ты отправил картинку, я сохраню ее себе")
    file = await bot.get_file(message.photo[-1].file_id)
    await bot.download_file(file.file_path, f"{message.from_user.username}.jpg")


async def get_hello(message: Message, bot: Bot):
    await message.answer(f"И тебе привет!)")
    if file_path:
        with open(file_path, "a", encoding="utf-8") as f:
            json_str = json.dumps(message.dict(), indent=4, default=str)
            f.write(json_str)
    else:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write()
