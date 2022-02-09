import secrets
from typing import List, Union
from pydantic import AnyHttpUrl, BaseSettings, validator
import os


class Settings(BaseSettings):
    
    ELASTICSEARCH_URL: str = os.getenv("ELASTICSEARCH_URL")
         

    class Config:
        case_sensitive = True

settings = Settings()