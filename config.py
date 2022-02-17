import secrets
from typing import List, Union
from pydantic import AnyHttpUrl, BaseSettings, validator
import os


class Settings(BaseSettings):
    
    ELASTICSEARCH_URL: str = os.getenv("ELASTICSEARCH_URL")
    SURVEYINTERLINK_URL: str = os.getenv("SURVEYINTERLINK_URL")
    SURVEYAPI_VERSION : str = os.getenv("SURVEYAPI_VERSION")
    PORTAUGMENTER: str = os.getenv("PORTAUGMENTER")
    

    class Config:
        case_sensitive = True

settings = Settings()