# Pydantic
from pydantic import BaseModel


class ResponseSchema(BaseModel):
    response: str


class ErrorSchema(BaseModel):
    error: str
