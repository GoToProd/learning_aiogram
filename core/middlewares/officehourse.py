from datetime import datetime
from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Callable, Dict, Any, Awaitable


def office_hourse() -> bool:
    return datetime.now().weekday() in (0, 1, 2, 3, 4) and datetime.now().hour in (
        [i for i in range(8, 19)]
    )


class OfficeHourseMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        if office_hourse():
            return await handler(event, data)

        await event.answer(
            f"Время работы бота:\r\n ПН-ПТ с 8 до 18. Приходите в рабочие часы."
        )
