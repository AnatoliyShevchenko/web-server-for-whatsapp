# Local
from src.settings.base import session


async def get_async_session():
    async with session() as conn:
        yield conn
        