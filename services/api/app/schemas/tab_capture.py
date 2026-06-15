from pydantic import BaseModel, HttpUrl

class TabCaptureRequest(BaseModel):
    browser_tab_id: int
    title: str
    url: HttpUrl
    favicon: str | None = None