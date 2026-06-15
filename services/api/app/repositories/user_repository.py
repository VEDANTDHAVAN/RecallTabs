from sqlalchemy.orm import Session
from app.infrastructure.database.models.user import User

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_clerk_id(self, clerk_user_id: str) -> User | None:
        return (
            self.db.query(User).filter(
                User.clerk_user_id == clerk_user_id
            ).first()
        )
    
    def create(self, clerk_user_id: str, email: str) -> User:
        user = User(
            clerk_user_id=clerk_user_id, email=email,
        )

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user