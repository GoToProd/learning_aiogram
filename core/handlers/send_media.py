import os
from aiogram import Bot
from aiogram.types import Message, FSInputFile, InputMediaPhoto, InputMediaVideo
from aiogram.utils.chat_action import ChatActionSender
from aiogram.dispatcher.event.handler import HandlerObject


async def get_audio(message: Message, bot: Bot):
    audio = FSInputFile(
        path=os.path.abspath("cicada_night_forest.mp3"), filename="AudioFile.mp3"
    )
    await bot.send_audio(message.chat.id, audio=audio)


async def get_document(message: Message, bot: Bot):
    document = FSInputFile(
        path=os.path.abspath("document.docx"), filename="Document.docx"
    )
    await bot.send_document(message.chat.id, document=document, caption="Its document")


async def get_media_group(message: Message, bot: Bot):
    photo1_mg = InputMediaPhoto(
        type="photo",
        media=FSInputFile(path=os.path.abspath("dan4eg.jpg")),
        caption="Its MEdiaGroup",
    )
    photo2_mg = InputMediaPhoto(
        type="photo",
        media=FSInputFile(path=os.path.abspath("priroda.png")),
    )
    video_mg = InputMediaVideo(
        type="video", media=FSInputFile(path=os.path.abspath("video.mp4"))
    )
    media = [photo1_mg, photo2_mg, video_mg]
    await bot.send_media_group(message.chat.id, media)


async def get_photo(message: Message, bot: Bot):
    photo = FSInputFile(path=os.path.abspath("dan4eg.jpg"))
    await bot.send_photo(message.chat.id, photo=photo, caption="Its photo!")


async def get_sticker(message: Message, bot: Bot):
    sticker = FSInputFile(path=os.path.abspath("priroda.png"))
    await bot.send_sticker(message.chat.id, sticker)


async def get_video(message: Message, bot: Bot, handler: HandlerObject):
    print(handler.flags)
    # async with ChatActionSender.upload_video(chat_id=message.chat.id, bot=bot):
    video = FSInputFile(path=os.path.abspath("video.mp4"))
    await bot.send_video(message.chat.id, video)


async def get_video_note(message: Message, bot: Bot):
    # async with ChatActionSender.upload_video_note(chat_id=message.chat.id, bot=bot):
    video_note = FSInputFile(path=os.path.abspath("video.mp4"))
    await bot.send_video_note(message.chat.id, video_note)


async def get_voice(message: Message, bot: Bot):
    # async with ChatActionSender.record_voice(message.chat.id, bot=bot):
    voice = FSInputFile(path=os.path.abspath("voice.opus"))
    await bot.send_voice(message.chat.id, voice)
