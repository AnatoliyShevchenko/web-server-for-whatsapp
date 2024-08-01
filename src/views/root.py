# FastAPI
from fastapi import APIRouter, status
from fastapi.responses import PlainTextResponse


class MainView:
    """View for main router."""

    def __init__(self) -> None:
        self.path = "/"
        self.router = APIRouter(tags=["Just need"])
        self.router.add_api_route(
            path=self.path, endpoint=self.main,
            methods=["GET"], responses={
                200: {"model": None}
            }
        )
    
    @staticmethod
    async def main():
        return PlainTextResponse(
            content="Nothing to see here."
            "\nCheckout README.md to start.", 
            status_code=status.HTTP_200_OK
        )
    

main_view = MainView()
