from typing import Callable, Dict, Any, Awaitable

# import asyncpg
from psycopg_pool import AsyncConnectionPool
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from core.utils.dbconnect import Request


class DbSession(BaseMiddleware):
    # def __init__(self, connector: asyncpg.pool.Pool):
    def __init__(self, connector: AsyncConnectionPool):
        super().__init__()
        self.connector = connector

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        # async with self.connector.acquire() as connect:
        async with self.connector.connection() as connect:
            data["request"] = Request(connect)
            return await handler(event, data)
