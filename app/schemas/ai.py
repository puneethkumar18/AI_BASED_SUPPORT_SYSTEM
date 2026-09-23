from pydantic import BaseModel
from enum import Enum


class TicketAnalysis(BaseModel):
    category: str
    priority: str
    summary: str
    suggested_resolution: str


class TicketPriority(str,Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"



class TicketCategory(str, Enum):
    AUTHENTICATION = "Authentication"
    DATABASE = "Database"
    NETWORK = "Network"
    HARDWARE = "Hardware"
    SOFTWARE = "Software"
    EMAIL = "Email"
    SECURITY = "Security"
    GENERAL = "General"