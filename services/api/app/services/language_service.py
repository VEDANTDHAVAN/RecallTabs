from lingua import LanguageDetectorBuilder

class LanguageService:
    def __init__(self):
        self.detector = (
            LanguageDetectorBuilder.from_all_languages().build()
        )

    async def detect(
        self, text: str,
    ) -> str:
        language = self.detector.detect_language_of(text)

        if language is None:
            return "Unknown"

        return language.iso_code_639_1.name.lower()