from pydantic import BaseModel

class SearchRequest(BaseModel):
    query: str

class SearchResult(BaseModel):
    tab_id: str
    title: str
    url: str
    score: float