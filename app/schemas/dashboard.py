from pydantic import BaseModel


class DashboardSummary(BaseModel):
    total_tickets:int
    open_tickets: int
    in_progress: int
    closed: int


class PriorityStatistics(BaseModel):
    priority: str
    count: int

class CategoryStatistics(BaseModel):
    category: str
    count: int

class AgentPerformance(BaseModel):
    agent_id: int
    agent_name: str
    assigned: int
    closed:int