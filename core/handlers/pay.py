from aiogram import Bot
from aiogram.types import (
    Message,
    LabeledPrice,
    PreCheckoutQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ShippingOption,
    ShippingQuery,
)


keyboards = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Оплатить заказ", pay=True)],
        [InlineKeyboardButton(text="Link", url="https://t.me/dan4eg")],
    ]
)


BY_SHIPPING = ShippingOption(
    id="by",
    title="Доставка в Беларусь",
    prices=[LabeledPrice(label="Доставка Белпочтой", amount=500)],
)

RU_SHIPPING = ShippingOption(
    id="ru",
    title="Доставка в России",
    prices=[LabeledPrice(label="Доставка ПочтаРоссии", amount=1000)],
)


UA_SHIPPING = ShippingOption(
    id="ua",
    title="Доставка в Украину",
    prices=[LabeledPrice(label="Доставка Укрпштой", amount=1500)],
)

CITIES_SHIPPING = ShippingOption(
    id="capitals",
    title="Быстрая доставка по городу",
    prices=[LabeledPrice(label="Доставка курьером Torretto", amount=2000)],
)


async def shipping_check(shipping_query: ShippingQuery, bot: Bot):
    shipping_options = []
    countries = ["BY", "RU", "UA"]
    if shipping_query.shipping_address.country_code not in countries:
        return await bot.answer_shipping_query(
            shipping_query.id, ok=False, error_message="В вашу страну нет доставки"
        )
    if shipping_query.shipping_address.country_code == "BY":
        shipping_options.append(BY_SHIPPING)
    if shipping_query.shipping_address.country_code == "RU":
        shipping_options.append(RU_SHIPPING)
    if shipping_query.shipping_address.country_code == "UA":
        shipping_options.append(UA_SHIPPING)

    cities = ["Минск", "Москва", "Киев"]
    if shipping_query.shipping_address.city in cities:
        shipping_options.append(CITIES_SHIPPING)

    await bot.answer_shipping_query(
        shipping_query.id, ok=True, shipping_options=shipping_options
    )


async def order(message: Message, bot: Bot):
    await bot.send_invoice(
        chat_id=message.chat.id,
        title="Покупка через Telegram бота",
        description="Учимся принимать платежи через Telegram бота",
        payload="Payment throuth a bot",
        provider_token="381764678:TEST:91691",
        currency="rub",
        prices=[
            LabeledPrice(label="Доступ к секретной информации", amount=99000),
            LabeledPrice(label="НДС", amount=20000),
            LabeledPrice(label="Скидка", amount=20000),
            LabeledPrice(label="Бонус", amount=-40000),
        ],
        max_tip_amount=5000,
        suggested_tip_amounts=[1000, 2000, 3000, 4000],
        start_parameter="gotoprod",
        provider_data=None,
        photo_url=None,
        photo_size=None,
        photo_height=None,
        photo_width=None,
        need_name=False,
        need_phone_number=False,
        need_email=False,
        need_shipping_address=False,
        send_phone_number_to_provider=False,
        send_email_to_provider=False,
        is_flexible=True,
        disable_notification=False,
        protect_content=False,
        reply_to_message_id=None,
        allow_sending_without_reply=True,
        reply_markup=keyboards,
        request_timeout=15,
    )


async def pre_checkout_query(pre_checkout_query: PreCheckoutQuery, bot: Bot):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


async def successful_payment(message: Message):
    msg = (
        f"Спасибо за оплату {message.successful_payment.total_amount // 100} {message.successful_payment.currency}."
        f"\r\n Наш менеджер получил заявку и уже набирает Ваш номер телефона."
        f"\r\n Пока можете скачать цифровую версию нашего продукта https://dan4eg.ru"
    )
    await message.answer(msg)
