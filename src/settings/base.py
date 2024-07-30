# FastAPI
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# SQL
from sqlalchemy.ext.asyncio import (
    create_async_engine, async_sessionmaker,
)

# Python
import logging
from logging.config import dictConfig

# Local
from .const import DB_URL


app = FastAPI(title="WhatsApp Web Server", debug=True)
app.add_middleware(
    middleware_class=CORSMiddleware, 
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=[
        "Accept", "Accept-Language", "Content-Language", "Content-Type"
    ]
)
engine = create_async_engine(url=DB_URL)
session = async_sessionmaker(
    bind=engine, expire_on_commit=False,
)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "detailed",
        },
    },
    "formatters": {
        "detailed": {
            "format": "%(asctime)s - %(levelname)s - %(name)s - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}
dictConfig(LOGGING)
logger = logging.getLogger(__name__)
