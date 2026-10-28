from functools import lru_cache

import jwt
from jwt import PyJWKClient

from app.core.config import get_settings

settings = get_settings()


@lru_cache(maxsize=1)
def get_jwt_client() -> PyJWKClient:
    return PyJWKClient(settings.CLERK_JWKS_URL)


def verify_token(token: str) -> dict:
    """Verify a Clerk JWT: signature, issuer, audience, expiration.

    Raises jwt.InvalidTokenError subclasses on any failure.
    """
    if not token:
        raise jwt.InvalidTokenError("Missing token")

    if not settings.CLERK_AUDIENCE:
        raise jwt.InvalidTokenError("CLERK_AUDIENCE is not configured")
    if not settings.CLERK_ISSUER:
        raise jwt.InvalidTokenError("CLERK_ISSUER is not configured")
    if not settings.CLERK_JWKS_URL:
        raise jwt.InvalidTokenError("CLERK_JWKS_URL is not configured")

    signing_key = get_jwt_client().get_signing_key_from_jwt(token)

    decode_options = {
        "verify_aud": True,
        "verify_iss": True,
        "verify_exp": True,
    }

    payload = jwt.decode(
        token,
        signing_key.key,
        algorithms=["RS256"],
        issuer=settings.CLERK_ISSUER,
        audience=settings.CLERK_AUDIENCE,
        options=decode_options,
        leeway=30,
    )

    if payload.get("sub") is None:
        raise jwt.InvalidTokenError("Missing subject claim")

    return payload
