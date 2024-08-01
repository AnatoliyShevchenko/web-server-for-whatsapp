# Python
import json


def get_headers_from_token(wa_token: str) -> dict:
    return {
        "Content-Type": "application/json", 
        "Authorization": f"Bearer {wa_token}"
    }

def form_sample_message(
    phone_num: str, sample_name: str, lang_code: str = "ru"
) -> str:
    data = {
        "messaging_product": "whatsapp",
        "to": phone_num,
        "type": "template",
        "template": {
            "name": sample_name,
            "language": {
                "code": lang_code
            }
        }
    }
    return json.dumps(obj=data)
