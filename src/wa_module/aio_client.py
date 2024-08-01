# AioHTTP
from aiohttp import ClientSession, ClientResponse, ClientError

# Python
from typing import Optional

# Local
from src.settings.base import logger


class AioClient:
    
    def __init__(self) -> None:
        self._session: Optional[ClientSession] = None

    async def create_session(self) -> ClientSession:
        if not self._session:
            self._session = ClientSession()
        
        return self._session
    
    async def close_session(self):
        if self._session:
            await self._session.close()
            self._session = None

    async def make_post_request(
        self, url: str, headers: dict, 
        data: dict = None, json: dict = None
    ) -> ClientResponse:
        session = await self.create_session()
        try:
            if json:
                response = await session.post(
                    url=url, headers=headers, json=json
                )
            elif data:
                response = await session.post(
                    url=url, headers=headers, data=data
                )
            logger.info(msg=f"Response status for URL: {url}"
                    f" is: {response.status}")
            return response
        except ClientError as ce:
            logger.error(msg="Client Error happend:", exc_info=ce)
        except Exception as e:
            logger.error(msg="Unknown error:", exc_info=e)
        return None
