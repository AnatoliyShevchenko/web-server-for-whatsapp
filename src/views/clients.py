# FastAPI
from fastapi import APIRouter, Depends, status, Response, UploadFile

# Thirt-Party
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert

# Python
from typing import Literal

# Local
from src.schemas.clients import ClientSchema, AllClientsSchema
from src.schemas.base import ResponseSchema, ErrorSchema
from src.utils.session import get_async_session
from src.utils.user_data_processing import UserDataProcessing
from src.models.clients import Clients


class ClientsView(UserDataProcessing):
    """View for Client's data."""

    def __init__(self) -> None:
        self.path = "/clients"
        self.router = APIRouter(tags=["View/Recieve Clients"])
        self.router.add_api_route(
            path=self.path, endpoint=self.add_client, methods=["POST"],
            responses={
                200: {"model": ResponseSchema},
                400: {"model": ErrorSchema}
            }
        )
        self.router.add_api_route(
            path=self.path, endpoint=self.get_all_clients, methods=["GET"],
            responses={
                200: {"model": AllClientsSchema},
                404: {"model": None}
            }
        )
        self.router.add_api_route(
            path=self.path+"/from_file", endpoint=self.create_clients_from_file, 
            methods=["POST"], responses={
                200: {"model": ResponseSchema},
                500: {"model": ErrorSchema}
            }
        )

    async def add_client(
        self, wa_number: str, wa_id: str, response: Response,
        session: AsyncSession = Depends(get_async_session)
    ):
        query = select(Clients).where(Clients.wa_id == wa_id)
        temp = await session.execute(query)
        client = temp.scalar()
        if client:
            response.status_code=status.HTTP_400_BAD_REQUEST
            return ErrorSchema(
                error=f"The client with wa_id: {wa_id} is already exist!"
            )
        stmt = insert(Clients).values(wa_number=wa_number, wa_id=wa_id)
        await session.execute(statement=stmt)
        await session.commit()
        return ResponseSchema(
            response=f"The client with wa_id: {wa_id} success added!"
        )
    
    async def get_all_clients(
        self, page_number: int = 0, confirmed: Literal["True", "False"] = None,
        session: AsyncSession = Depends(get_async_session)
    ):
        query = select(Clients).limit(100).offset(page_number)
        if confirmed == "True":
            query = query.where(Clients.confirm==True)
        elif confirmed == "False":
            query = query.where(Clients.confirm==False)
        temp = await session.execute(query)
        data = temp.scalars().all()
        if not data:
            return Response(status_code=status.HTTP_404_NOT_FOUND)
        obj = []
        for item in data:
            obj.append(ClientSchema(
                id=item.id, wa_number=item.wa_number, 
                wa_id=item.wa_id, confirm=item.confirm
            ))
        result = AllClientsSchema(clients=obj)
        return result
    
    async def create_clients_from_file(
        self, response: Response, file: UploadFile,
        session: AsyncSession = Depends(get_async_session)
    ):
        file_path = await self.save_file_to_volume(file=file)
        result = await self.get_chunks(
            file_path=file_path, session=session
        )
        if result == "Success":
            return ResponseSchema(response=result)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return ErrorSchema(error=result)


clients_view = ClientsView()
