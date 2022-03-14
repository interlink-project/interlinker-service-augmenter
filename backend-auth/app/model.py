from datetime import datetime
from pydantic import BaseModel, Extra, root_validator
from typing import Optional
from app.config import settings

class UserSchema(BaseModel, extra=Extra.ignore):
    _id: str
    sub: str
    picture: Optional[str]
    full_name: Optional[str]
    last_login: datetime = datetime.now()
    email: str
    zoneinfo: Optional[str]
    locale: Optional[str]
    
class UserOutSchema(UserSchema, extra=Extra.ignore):
    given_name: Optional[str]

    @root_validator(pre=True)
    def update_picture_uri_if_static(cls, values):
        if "picture" in values and values["picture"] and "/static" in values["picture"]:
            newValues = {**values}
            newValues["picture"] = settings.COMPLETE_SERVER_NAME + newValues["picture"]
            return newValues
        return values