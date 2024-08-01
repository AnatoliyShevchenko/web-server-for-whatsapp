# AioHTTP
from aiohttp import ClientError, ClientResponse

# Local
from .aio_client import AioClient
from .message import form_sample_message, get_headers_from_token
from src.settings.base import logger
from src.settings.const import NUMBER_ID, TEMP_TOKEN


class Whatsapp:

    def __init__(
        self, number_id: str = NUMBER_ID, 
        token: str = TEMP_TOKEN, version_number: str = "v20.0"
    ) -> None:
        self.id = number_id
        self.token = token
        self.version_number = version_number
        self.client = AioClient()
        self.base_url = f"https://graph.facebook.com/{self.version_number}/{self.id}"
        self.msg_url = self.base_url + "/messages"
        self.media_url = self.base_url + "/media"

    async def send_sample_text_message(
        self, recipient_phone_number: str, 
        sample_name: str, lang_code: str
    ):
        data = form_sample_message(
            phone_num=recipient_phone_number, sample_name=sample_name,
            lang_code=lang_code
        )
        headers = get_headers_from_token(wa_token=self.token)
        status, response_data = await self.processing_response(
            headers=headers, data=data
        )
        return status, response_data
    
    async def processing_response(self, headers: dict, data: str):
        response_data = {}
        try:
            response: ClientResponse = \
                await self.client.make_post_request(
                    url=self.msg_url, headers=headers, data=data
                )
            response_data = await response.json()
            if response.status == 200:
                logger.info(msg=f"Message id: {response_data["messages"][0]["id"]}")
            elif response.status == 401:
                logger.error(msg="Cannot make request, "
                        "check your number_id or token!")
            else:
                logger.error(
                    msg=f"Unknown error with code: {response.status}"
                )
        except ClientError as ce:
            logger.error(msg="Client Error happend:", exc_info=ce)
        except Exception as e:
            logger.error(msg="Unknown error:", exc_info=e)
        finally:
            await self.client.close_session()
            return response.status, response_data
