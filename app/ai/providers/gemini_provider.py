from app.ai.providers.interface import LLMProvider
from google import genai
from app.core.config import settings
from app.schemas.ai import TicketAnalysis
from app.ai.prompts import TICKET_ANALYSIS_PROMPT
import json
from app.exceptions.custom_exception import LLMException


class GeminiProvider(LLMProvider):

    def __init__(self):
        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )

    async def analyze_ticket(self, title, description):
        prompt = f"""
            {TICKET_ANALYSIS_PROMPT}

            Title:
            {title}

            Description:
            {description}

            """
        try:
            response = await self.client.aio.models.generate_content(
                model="gemini-3.5-flash",
                contents=prompt
            )
        except Exception as e:
            raise LLMException(str(e)) from e

        text = response.text.strip()

        if text.startswith("```json"):
            text = text.replace("```json", "").replace("```", "").strip()

        elif text.startswith("```"):
            text = text.replace("```", "").strip()

        data = json.loads(text)

        return TicketAnalysis.model_validate(data)
        

        