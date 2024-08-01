# Pydantic
from pydantic import BaseModel, Field


class ClientSchema(BaseModel):
    id: int = Field(ge=0)
    wa_number: str
    wa_id: str
    confirm: bool


class AllClientsSchema(BaseModel):
    clients: list[ClientSchema]
    