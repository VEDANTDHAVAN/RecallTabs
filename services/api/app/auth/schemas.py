from pydantic import BaseModel

class ClerkUser(BaseModel):
    sub: str
    email: str | None = None