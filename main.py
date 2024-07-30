# Third-Party
import uvicorn
import asyncio

# Local
from src.settings.base import logger, app
from src.views.webhooks import webhooks_view


async def main():
    app.include_router(router=webhooks_view.router)
    config = uvicorn.Config(
        app="main:app", host="0.0.0.0", 
        port=8000, reload=True
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
        