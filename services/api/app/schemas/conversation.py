from pydantic import BaseModel

class ConversationCreate(BaseModel):
    title: str | None

class ConversationUpdate(BaseModel):
    title: str

class ConversationResponse(BaseModel):
    id: str
    title: str | None

    class Config:
        from_attributes = True