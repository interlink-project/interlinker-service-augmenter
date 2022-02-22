import secrets
from typing import List, Union
from pydantic import AnyHttpUrl, BaseSettings, validator
import os


class Settings(BaseSettings):
    
    ELASTICSEARCH_URL: str = os.getenv("ELASTICSEARCH_URL")
    SURVEYINTERLINK_URL: str = os.getenv("SURVEYINTERLINK_URL")
    SURVEYAPI_VERSION : str = os.getenv("SURVEYAPI_VERSION")
    PORTAUGMENTER: str = os.getenv("PORTAUGMENTER")
    HOSTAUGMENTER: str = os.getenv("HOSTAUGMENTER")


    DEBUG: bool = os.getenv("DEBUG")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ELASTICSEARCH_INDEX:str = os.getenv("ELASTICSEARCH_INDEX")
    AUTH_ON: bool = os.getenv("AUTH_ON")
    AUTHZ_ON: bool = os.getenv("AUTHZ_ON")
  


    # Mail server configuration Parameters:
    MAIL_SERVER:str = os.getenv("MAIL_SERVER")
    MAIL_PORT:int = os.getenv("MAIL_PORT")
 
    MAIL_USERNAME:str = os.getenv("MAIL_USERNAME") 
    MAIL_PASSWORD:str = os.getenv("MAIL_PASSWORD") 
    MAIL_DEFAULT_SENDER:str = os.getenv("MAIL_DEFAULT_SENDER") 
    MAIL_USE_TLS: bool = os.getenv("MAIL_USE_TLS")
    MAIL_USE_SSL: bool = os.getenv("MAIL_USE_SSL")
    MAIL_MAX_EMAILS:str = os.getenv("MAIL_MAX_EMAILS")
    MAIL_ASCII_ATTACHMENTS: bool = os.getenv("MAIL_ASCII_ATTACHMENTS")

    MAX_CONTENT_LENGTH: int = os.getenv("MAX_CONTENT_LENGTH") 
    UPLOAD_EXTENSIONS: List[str] = os.getenv("UPLOAD_EXTENSIONS")
    UPLOAD_PATH:str = os.getenv("UPLOAD_PATH") 
    USE_SESSION_FOR_NEXT: bool = os.getenv("USE_SESSION_FOR_NEXT")

    # Swagger parameters:

    SWAGGER_URL:str = os.getenv("SWAGGER_URL")
    API_URL:str = os.getenv("API_URL")

    #Babel:
    BABEL_DEFAULT_LOCALE:str = os.getenv("BABEL_DEFAULT_LOCALE")



    #Parametros de Autenticacion:

    CLIENT_ID:str = os.getenv("CLIENT_ID")
    CLIENT_SECRET:str = os.getenv("CLIENT_SECRET")
    ISSUER:str = os.getenv("ISSUER")

    AUTH_URI:str = os.getenv("AUTH_URI")
    TOKEN_URI:str = os.getenv("TOKEN_URI")
    TOKEN_INTROSPECTION_URI:str = os.getenv("TOKEN_INTROSPECTION_URI")

    REDIRECT_URI:str = os.getenv("REDIRECT_URI")
    
    USERINFO_URI:str = os.getenv("USERINFO_URI")

    END_SESSION_ENDPOINT:str = os.getenv("END_SESSION_ENDPOINT")

    CONSUMER_KEY:str = os.getenv("CONSUMER_KEY")
    CONSUMER_TTL: int = os.getenv("CONSUMER_TTL")
    CRYPT_KEY:str = os.getenv("CRYPT_KEY")




    class Config:
        case_sensitive = True

settings = Settings()