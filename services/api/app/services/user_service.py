from sqlalchemy.orm import Session

from app.repositories.user_repository import UserRepository

class UserProvisioningService:
    def __init__(self, db: Session,):
        self.repo = UserRepository(db)
    
    def get_or_create_user(self, clerk_user_id: str, email: str):
        user = self.repo.get_by_clerk_id(
            clerk_user_id
        )

        if user:
            return user
        
        return self.repo.create(
            clerk_user_id=clerk_user_id,
            email=email,
        )