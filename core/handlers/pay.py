from aiogram import Bot
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery


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
        need_name=True,
        need_phone_number=True,
        need_email=True,
        need_shipping_address=False,
        send_phone_number_to_provider=False,
        send_email_to_provider=False,
        is_flexible=False,
        disable_notification=False,
        protect_content=False,
        reply_to_message_id=None,
        allow_sending_without_reply=True,
        reply_markup=None,
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
