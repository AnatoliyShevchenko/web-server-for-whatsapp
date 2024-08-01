# FastApi
from fastapi import UploadFile

# Third-Party
import aiofiles
from sqlalchemy.ext.asyncio import AsyncSession

# Python
import os

# Local
from src.settings.const import VOLUME
from src.settings.base import logger
from src.models.clients import Clients
from src.schemas.clients import ClientSchema


class UserDataProcessing:

    @staticmethod
    async def create_clients_batch(
        clients_data: list[dict[str, str]], session: AsyncSession
    ) -> bool:
        try:
            async with session.begin():
                clients = [Clients(**data) for data in clients_data]
                session.add_all(clients)
                await session.commit()
            return True
        except Exception as e:
            logger.error(
                msg="Cannot create clients batch:", exc_info=e
            )
            return False

    @staticmethod
    async def save_file_to_volume(file: UploadFile):
        file_path = os.path.join(VOLUME, file.filename)
        async with aiofiles.open(file_path, 'wb') as out_file:
            while True:
                chunk = await file.read(1024 * 1024)
                if not chunk:
                    break
                await out_file.write(chunk)
        return file_path

    async def get_chunks(self, file_path: str, session: AsyncSession):
        lines = []
        try:
            async with aiofiles.open(file=file_path) as file:
                iteration = 0
                async for line in file:
                    if len(lines) >= 100:
                        await self.create_clients_batch(
                            clients_data=lines, session=session
                        )
                        iteration += 1
                        logger.info(
                            msg=f"Iteration {iteration} success!"
                        )
                        lines.clear()
                    try:
                        wa_number, wa_id = line.split(" ")
                        schema = ClientSchema(
                            wa_number=wa_number.strip(),
                            wa_id=wa_id.strip()
                        )
                        temp = schema.model_dump()
                        lines.append(temp)
                    except ValueError as ve:
                        logger.error(
                            f"Error processing line: {line.strip()} - {ve}"
                        )

                if lines:
                    await self.create_clients_batch(
                        clients_data=lines, session=session
                    )
                    logger.info(msg="Last iteration success!")
            return "Success"
        except Exception as e:
            return str(e)
        