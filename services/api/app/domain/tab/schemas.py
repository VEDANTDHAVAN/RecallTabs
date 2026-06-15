from pydantic import BaseModel, HttpUrl

class CreateTabRequest(BaseModel):
    url: HttpUrl
    title: str
    content: str | None = None

class TabResponse(BaseModel):
    id: str
    user_id: str
    url: str
    title: str
    content: str | None

    model_config = {
        "from_attributes": True
    }