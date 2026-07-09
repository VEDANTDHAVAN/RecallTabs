from enum import Enum

class RetrievalIntent(str, Enum):
    FACT = "fact"
    HISTORY = "history"
    RESEARCH = "research"
    BROWSING = "browsing"
    GENERAL = "general"

class RetrievalIntentService:
    def classify(self, question: str) -> RetrievalIntent:
        q = question.lower()

        if any(
            word in q for word in [
                "when", "last time", "previous",
                "earlier", "history",
            ]
        ):
            return RetrievalIntent.HISTORY
        
        if any(
            word in q for word in [
                "paper", "research", "study", "explain",
            ]
        ):
            return RetrievalIntent.RESEARCH
        
        if any(
            word in q for word in [
                "tab", "page", "website", "browser",
            ]
        ):
            return RetrievalIntent.BROWSING
        
        if any(
            word in q for word in [
                "what", "who", "define",
            ]
        ):
            return RetrievalIntent.FACT
        
        return RetrievalIntent.GENERAL