from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from core.utils.callbackdata import MacInfo


select_macbook = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Macbook Air 13", callback_data="apple_air_13_m1_2020"
            )
        ],
        [
            InlineKeyboardButton(
                text="Macbook Pro 14", callback_data="apple_pro_14_m2_2022"
            )
        ],
        [
            InlineKeyboardButton(
                text="Macbook Pro 16", callback_data="apple_pro_16_m3_2023"
            )
        ],
        [InlineKeyboardButton(text="Link", url="https://www.apple.com/")],
        [InlineKeyboardButton(text="Telega", url="tg://user?id=1110147997")],
    ]
)


def get_inline_keyboard():
    keyboard_builder = InlineKeyboardBuilder()

    keyboard_builder.button(
        text="Macbook Air 13",
        callback_data=MacInfo(model="air", size="13", chip="m1", year="2020"),
    )
    keyboard_builder.button(
        text="Macbook Pro 14",
        callback_data=MacInfo(model="pro", size="14", chip="m2", year="2022"),
    )
    keyboard_builder.button(
        text="Macbook Pro 16",
        callback_data=MacInfo(model="max", size="16", chip="m3", year="2023"),
    )
    keyboard_builder.button(text="Link", url="https://www.apple.com/")
    keyboard_builder.button(text="Telega", url="tg://user?id=1110147997")

    keyboard_builder.adjust(3)

    return keyboard_builder.as_markup()
