from fastapi import APIRouter, FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import (
    close_mongo_connection,
    connect_to_mongo,
)
from app.api.v1.integrable import integrablerouter
from app.api.v1.custom import customrouter

app = FastAPI(
    title="Survey interlinker API", openapi_url=f"/openapi.json", docs_url="/docs", root_path=settings.BASE_PATH
)
app.add_event_handler("startup", connect_to_mongo)
app.add_event_handler("shutdown", close_mongo_connection)

app.mount("/static", StaticFiles(directory="static"), name="static")

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

mainrouter = APIRouter()


@mainrouter.get("/")
def main():
    return RedirectResponse(url=f"{settings.BASE_PATH}/docs")


@mainrouter.get("/healthcheck")
def healthcheck():
    return True


app.include_router(mainrouter, tags=["main"])
app.include_router(integrablerouter, tags=["Integrable"])
app.include_router(customrouter, prefix=settings.API_V1_STR, tags=["Custom endpoints"])
