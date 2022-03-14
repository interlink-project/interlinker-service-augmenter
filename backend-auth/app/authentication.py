import jwt
from app.config import settings
from authlib.integrations.starlette_client import OAuth
from jwt import PyJWKClient

url = "https://aac.platform.smartcommunitylab.it/jwk"

oauth = OAuth()
oauth.register(
    name='smartcommunitylab',
    client_id=settings.CLIENT_ID,
    client_secret=settings.CLIENT_SECRET,
    server_metadata_url=settings.SERVER_METADATA_URL,
    client_kwargs={
        'scope': 'openid profile email'
    }
)

def decode_token(jwtoken):
    jwks_client = PyJWKClient(url)
    signing_key = jwks_client.get_signing_key_from_jwt(jwtoken)
    data = jwt.decode(
        jwtoken,
        signing_key.key,
        algorithms=["RS256"],
        audience="c_0e0822df-9df8-48d6-b4d9-c542a4623f1b",
        # options={ 'verify_nbf': False}
    )
    return data