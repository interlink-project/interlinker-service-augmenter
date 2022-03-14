from fastapi.templating import Jinja2Templates
from app.config import settings

templates = Jinja2Templates(directory="templates")
domainfo = {
        "PROTOCOL": settings.PROTOCOL,
        "SERVER_NAME": settings.SERVER_NAME ,
        "BASE_PATH": settings.BASE_PATH ,
        "COMPLETE_SERVER_NAME": settings.COMPLETE_SERVER_NAME 
    }