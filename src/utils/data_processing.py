def get_message_from_body(body: dict):
    entry = body.get("entry", [{}])[0]
    changes = entry.get("changes", [{}])[0]
    value = changes.get("value", {})
    message = value.get("messages", [{}])[0]
    return message

def get_business_phone_number_id(body: dict):
    entry = body.get("entry", [{}])[0]
    changes = entry.get("changes", [{}])[0]
    value = changes.get("value", {})
    metadata = value.get("metadata", {})
    phone_number_id = metadata.get("phone_number_id")
    return phone_number_id

def get_button_data(body: dict):
    entry = body["entry"][0]
    change = entry["changes"][0]
    message_value = change["value"]
    button = message_value["messages"][0]["button"]
    text: str = button.get("text")
    if text.startswith("Да,"):
        return True
    else:
        return False

def get_user_number(body: dict):
    entry = body["entry"][0]
    change = entry["changes"][0]
    message_value = change["value"]
    wa_id = message_value["contacts"][0]["wa_id"]
    return wa_id
