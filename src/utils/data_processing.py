# Local
from src.settings.base import logger


def get_message_from_body(body: dict):
    try:
        entry = body.get("entry", [{}])[0]
        changes = entry.get("changes", [{}])[0]
        value = changes.get("value", {})
        message = value.get("messages", [{}])[0]
        return message
    except Exception as e:
        logger.error(msg="Cannot get message from body:", exc_info=e)
        return None

def get_business_phone_number_id(body: dict):
    try:
        entry = body.get("entry", [{}])[0]
        changes = entry.get("changes", [{}])[0]
        value = changes.get("value", {})
        metadata = value.get("metadata", {})
        phone_number_id = metadata.get("phone_number_id")
        return phone_number_id
    except Exception as e:
        logger.error(msg="Cannot get number_id from body:", exc_info=e)
        return None

def get_button_data(body: dict):
    try:
        entry = body["entry"][0]
        change = entry["changes"][0]
        message_value = change["value"]
        button = message_value["messages"][0]["button"]
        text: str = button.get("text")
        if text.startswith("Да,"):
            return True
        else:
            return False
    except Exception as e:
        logger.error(msg="Cannot get button data from body:", exc_info=e)
        return None

def get_user_number(body: dict):
    try:
        entry = body["entry"][0]
        change = entry["changes"][0]
        message_value = change["value"]
        wa_id = message_value["contacts"][0]["wa_id"]
        return wa_id
    except Exception as e:
        logger.error(msg="Cannot get wa_id from body:", exc_info=e)
        return None
