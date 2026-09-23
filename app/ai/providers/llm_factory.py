from app.ai.providers.gemini_provider import GeminiProvider


class LLMFactory:
    @staticmethod
    def get_provider():
        return GeminiProvider()
