from enum import Enum

class SearchIntent(str, Enum):
    KEYWORD = "keyword"
    SEMANTIC = "semantic"
    DOMAIN = "domain"
    TITLE = "title"
    RECENT = "recent"
    TOPIC = "topic"
    HYBRID = "hybrid"

class SearchIntentService:
    def detect(self, query: str) -> SearchIntent:
        q = query.lower().strip()

        if "." in q and " " not in q:
            return SearchIntent.DOMAIN
        
        if q.startswith("www"):
            return SearchIntent.DOMAIN
        
        if any(x in q for x in [
            "today", "yesterday", "recent", "last"
        ]):
            return SearchIntent.RECENT
        
        if len(q.split()) == 1:
            return SearchIntent.KEYWORD
        
        if any(x in q for x in [
            "about", "related", "explain", "learn", "topic"
        ]):
            return SearchIntent.SEMANTIC
        
        return SearchIntent.HYBRID