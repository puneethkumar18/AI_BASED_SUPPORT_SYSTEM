from abc import ABC,abstractmethod
from app.schemas.ai import TicketAnalysis

class LLMProvider:

    @abstractmethod
    def analyze_ticket(self,title:str,description:str)->TicketAnalysis:
        pass