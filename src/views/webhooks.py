# FastAPI
from fastapi import APIRouter, Depends, status, Request, HTTPException
from fastapi.responses import PlainTextResponse

# Thirt-Party
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update

# Python
import json

# Local
from src.utils.session import get_async_session
from src.utils.data_processing import (
    get_message_from_body, get_user_number,
    get_business_phone_number_id, get_button_data,
)
from src.wa_module.aio_client import AioClient
from src.models.clients import Clients
from src.settings.base import logger
from src.settings.const import TEMP_TOKEN, WEBHOOK_VERIFY_TOKEN, GRAPH_API_TOKEN, NUMBER_ID


class WebhooksView:
    """View for Webhook's data."""

    def __init__(self) -> None:
        self.path = "/webhook"
        self.client = AioClient()
        self.router = APIRouter(tags=["View/Recieve Webhooks"])
        self.router.add_api_route(
            path=self.path, endpoint=self.verify_webhook,
            methods=["GET"], responses={
                200: {"model": None},
                403: {"model": None}
            }
        )
        self.router.add_api_route(
            path=self.path, endpoint=self.handle_webhook,
            methods=["POST"], responses={
                200: {"model": None}
            }
        )

    async def handle_webhook(
        self, request: Request,
        session: AsyncSession = Depends(get_async_session)
    ):
        temp = await request.body()
        body = json.loads(temp)
        logger.info(msg=f"Incoming webhook message: {temp}")
        
        message = get_message_from_body(body=body)
        if message.get("type") == "button":
            wa_id = get_user_number(body=body)
            button = get_button_data(body=body)
            if button:
                stmt = update(Clients).where(
                    Clients.wa_id == wa_id
                ).values(confirm=True)
                await session.execute(statement=stmt)
                await session.commit()
                logger.info(msg=f"{wa_id} updated!")
        try:
            await self.client.make_post_request(
                url=f"https://graph.facebook.com/v20.0/{NUMBER_ID}/messages",
                headers={"Authorization": f"Bearer {TEMP_TOKEN}"},
                json={
                    "messaging_product": "whatsapp",
                    "to": message["from"],
                    "text": {"body": "Echo: " + message["text"]["body"]},
                    "context": {"message_id": message["id"]}
                }
            )
        except Exception as e:
            logger.error(msg="Unknown error:", exc_info=e)
        try:
            await self.client.make_post_request(
                url=f"https://graph.facebook.com/v20.0/{NUMBER_ID}/messages",
                headers={"Authorization": f"Bearer {TEMP_TOKEN}"},
                json={
                    "messaging_product": "whatsapp",
                    "status": "read",
                    "message_id": message["id"]
                }
            )
        except Exception as e:
            logger.error(msg="Unknown error:", exc_info=e)

        return PlainTextResponse(status_code=200)
    
    async def verify_webhook(self, request: Request):
        params = request.query_params
        hub_mode = params.get("hub.mode")
        hub_verify_token = params.get("hub.verify_token")
        hub_challenge = params.get("hub.challenge")
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
