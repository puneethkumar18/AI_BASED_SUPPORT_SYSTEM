


from app.ai.providers.llm_factory import LLMFactory


class AIServices:

    @staticmethod
    async def analyze_ticket(title: str, description: str):
        provider = LLMFactory.get_provider()
        return await provider.analyze_ticket(
            title=title,
            description=description
        )

    