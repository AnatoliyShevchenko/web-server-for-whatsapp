# FastAPI
from fastapi import APIRouter, Depends, status, Request, HTTPException
from fastapi.responses import PlainTextResponse

# Thirt-Party
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, and_, insert

# Local
from src.utils.session import get_async_session
from src.utils.data_processing import (
    get_message_from_body, get_user_number,
    get_business_phone_number_id, get_button_data,
)
from src.utils.aio_client import AioClient
from src.models.clients import Clients
from src.settings.base import logger
from src.settings.const import GRAPH_API_TOKEN, WEBHOOK_VERIFY_TOKEN


class WebhooksView:
    """View for Webhook's data."""

    def __init__(self) -> None:
        self.path = "/webhook"
        self.client = AioClient()
        self.router = APIRouter(tags=["View/Recieve Webhooks"])
        self.router.add_api_route(
            path=self.path, endpoint=self.handle_webhook,
            methods=["POST"], responses={
                200: {"model": PlainTextResponse}
            }
        )
        self.router.add_api_route(
            path=self.path, endpoint=self.verify_webhook,
            methods=["GET"], responses={
                200: {"model": PlainTextResponse},
                403: {"model": None}
            }
        )

    async def handle_webhook(
        self, request: Request,
        session: AsyncSession = Depends(get_async_session)
    ):
        body = await request.json()
        logger.info(msg="Incoming webhook message: ", exc_info=body)
        
        message = get_message_from_body(body=body)

        if message.get("type") == "text":
            business_phone_number_id = \
                get_business_phone_number_id(body=body)
            wa_id = get_user_number(body=body)
            button = get_button_data(body=body)

            await self.client.make_post_request(
                url=f"https://graph.facebook.com/v18.0/{business_phone_number_id}/messages",
                headers={"Authorization": f"Bearer {GRAPH_API_TOKEN}"},
                json={
                    "messaging_product": "whatsapp",
                    "to": message["from"],
                    "text": {"body": "Echo: " + message["text"]["body"]},
                    "context": {"message_id": message["id"]}
                }
            )

            await self.client.make_post_request(
                url=f"https://graph.facebook.com/v18.0/{business_phone_number_id}/messages",
                headers={"Authorization": f"Bearer {GRAPH_API_TOKEN}"},
                json={
                    "messaging_product": "whatsapp",
                    "status": "read",
                    "message_id": message["id"]
                }
            )
            
            if button:
                stmt = update(Clients).where(
                    Clients.wa_id == wa_id
                ).values(confirm=True)
                await session.execute(statement=stmt)
                await session.commit()
                logger.info(msg=f"{wa_id} updated!")

        return PlainTextResponse(status_code=200)
    
    async def verify_webhook(
        self, hub_mode: str, hub_verify_token: str, hub_challenge: str
    ):
        if hub_mode == "subscribe" and \
            hub_verify_token == WEBHOOK_VERIFY_TOKEN:
            logger.info(msg="Webhook verified successfully!")
            return PlainTextResponse(
                content=hub_challenge, status_code=status.HTTP_200_OK
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="Forbidden"
            )


webhooks_view = WebhooksView()
