from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session

from app.domain.tab.schemas import CreateTabRequest, TabResponse
from app.repositories.tab_repository import TabRepository
from app.services.tab_service import TabService
from app.services.user_service import UserProvisioningService
from app.services.tab_capture_service import TabCaptureService
from app.infrastructure.database.session import get_db
from app.auth.dependencies import get_current_user
from app.schemas.tab_capture import TabCaptureRequest

router = APIRouter(prefix="/tabs", tags=["tabs"])

@router.get("/me")
def me(current_user=Depends(get_current_user),):
    return {
        "id": current_user.id,
        "email": current_user.email,
    }

@router.get("/debug-user")
def debug_user(db: Session = Depends(get_db)):
    service = UserProvisioningService(db)

    user = service.get_or_create_user(
        clerk_user_id="test-clerk-id",
        email="test@example.com",
    )

    return {
        "id": user.id,
        "email": user.email,
    }

@router.post("/capture")
def capture_tab(
    payload: TabCaptureRequest,
    db: Session = Depends(get_db),
    #current_user=Depends(get_current_user),
):
    service = TabCaptureService(db)

    tab = service.capture(
        payload=payload, user_id="125657ed-f496-4735-8391-696b96be49c8",
    )

    return {
        "id": str(tab.id),
        "title": tab.title,
    }

@router.post("", response_model=TabResponse,)
def create_tab(
    payload: CreateTabRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    repository = TabRepository(db)
    service = TabService(repository)

    return service.create_tab(
        user_id=current_user.id, payload=payload,
    )

@router.get("", response_model=list[TabResponse],)
def list_tabs(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    repository = TabRepository(db)
    service = TabService(repository)

    return service.list_tabs(user_id=current_user.id)
