import json
import os
from base64 import b64encode
import json
from uuid import UUID
from contextvars import ContextVar
import logging

from flask_login import current_user

import pika
from app.config import settings


_disable_logging: ContextVar[str] = ContextVar("disable_logging", default=False)

def set_logging_disabled(val: bool) -> str:
    try:
        _disable_logging.set(val)
    except:
        pass

def is_logging_disabled() -> str:
    return  _disable_logging.get()


class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            # if the obj is uuid, we simply return the value of uuid
            return obj.hex
        return json.JSONEncoder.default(self, obj)
        
exchange_name = settings.EXCHANGE_NAME
rabbitmq_host = settings.RABBITMQ_HOST
rabbitmq_user = settings.RABBITMQ_USER
rabbitmq_password = settings.RABBITMQ_PASSWORD


def log(data: dict):
    if is_logging_disabled():
        return

    try:
        #data["user_id"] = context.data.get("user", {}).get("sub", None)
        data["user_id"] = current_user.email
    except:
        data["user_id"] = None
    #data["service"] = "coproduction"

    request = b64encode(json.dumps(data,cls=UUIDEncoder).encode())

    logging.info('RabbitHost:'+rabbitmq_host)

    credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_password)
    parameters = pika.ConnectionParameters(host=rabbitmq_host,credentials=credentials)

    connection = pika.BlockingConnection(parameters)

    channel = connection.channel()


    channel.exchange_declare(
        exchange=exchange_name, exchange_type='direct'
    )

    channel.basic_publish(
        exchange=exchange_name,
        routing_key='logging', 
        body=request
    )