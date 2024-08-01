# FastAPI
from fastapi import APIRouter, Depends, status, HTTPException

# Thirt-Party
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import asyncio

# Python
from typing import Literal

# Local
from src.schemas.base import ResponseSchema
from src.utils.session import get_async_session
from src.models.clients import Clients
from src.wa_module.tasks import launch_task


class ScheduleView:
    """View for schedule data."""

    def __init__(self) -> None:
        self.path = "/schedule"
        self.router = APIRouter(tags=["View/Recieve Schedule"])
        self.router.add_api_route(
            path=self.path, endpoint=self.create_task, 
            methods=["POST"], responses={
                200: {"model": ResponseSchema},
                404: {"model": None}
            }
        )

    async def create_task(
        self, template_name: str, lang_code: str = "ru", 
        confirmed_users: Literal["True", "False"] = None,
        session: AsyncSession = Depends(get_async_session)
    ):
        query = select(Clients)
        if confirmed_users == "False":
            query = query.where(Clients.confirm == False)
        elif confirmed_users == "True":
            query = query.where(Clients.confirm == True)
        temp = await session.execute(query)
        data = temp.scalars().all()
        if not data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Clients not found"
            )
        asyncio.create_task(
            launch_task(
                clients=data, sample_name=template_name, 
                lang_code=lang_code
            )
        )
        return ResponseSchema(response="Task has been launched")
        

schedule_view = ScheduleView()
