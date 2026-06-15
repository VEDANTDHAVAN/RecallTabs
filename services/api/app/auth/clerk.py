from functools import lru_cache

import httpx
import jwt
from jwt import PyJWKClient

from app.core.config import get_settings

settings = get_settings()

@lru_cache(maxsize=1)
def get_jwt_client() -> PyJWKClient:
    return PyJWKClient(settings.CLERK_JWKS_URL)

def verify_token(token: str) -> dict:
    signing_key = get_jwt_client().get_signing_key_from_jwt(token)

    payload = jwt.decode(
        token, signing_key.key, algorithms=["RS256"],
        issuer=settings.CLERK_ISSUER, options={
            "verify_aud": False
        },
    )

    return payload