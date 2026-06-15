from fastapi import Depends, Header, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated

from app.auth.clerk import verify_token
from app.services.user_service import UserProvisioningService
from app.infrastructure.database.session import get_db

def get_current_user(
    authorization: Annotated[str | None, Header()] = None,
    db: Session = Depends(get_db),
):
    if not authorization:
        raise HTTPException(
            status_code=401, detail="Missing bearer token",
        )
    
    token = authorization.replace("Bearer ", "",)

    try:
        claims = verify_token(token)
        clerk_user_id = claims["sub"]
        email = claims.get("email")

        if not email:
            raise HTTPException(
                status_code=401, detail="Email missing",
            )
        
        service = UserProvisioningService(db)

        return service.get_or_create_user(
            clerk_user_id=clerk_user_id, email=email,
        )
    
    except Exception:
        raise HTTPException(
            status_code=401, detail="Invalid token",
        )