# Local
from .whatsapp import Whatsapp
from src.models.clients import Clients


async def launch_task(
    clients: list[Clients], sample_name: str, lang_code: str
):
    bot = Whatsapp()
    for i, client in enumerate(clients):
        status, response = await bot.send_sample_text_message(
            recipient_phone_number=client.wa_number, 
            sample_name=sample_name, lang_code=lang_code
        )
    