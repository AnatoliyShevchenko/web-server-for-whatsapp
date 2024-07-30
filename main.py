# Third-Party
import uvicorn
import asyncio

# Local
from src.settings.base import logger, app
from src.settings.const import PORT
from src.views.root import main_view
from src.views.webhooks import webhooks_view


async def main():
    app.include_router(router=main_view.router)
    app.include_router(router=webhooks_view.router)
    config = uvicorn.Config(
        app="main:app", host="0.0.0.0", port=PORT,
    )
    server = uvicorn.Server(config=config)
    logger.info(msg="SERVER STARTED")
    await server.serve()

async def shutdown():
    logger.info(msg="SHUTDOWN SERVER")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    finally:
        asyncio.run(shutdown())
        