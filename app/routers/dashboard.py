from fastapi import APIRouter,HTTPException,Depends
from app.schemas.dashboard import DashboardSummary,PriorityStatistics,CategoryStatistics,AgentPerformance
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.services.dashboard_services import DashboardService
from typing import List


router = APIRouter(prefix="/dashboard",tags=["Dashboard"])


@router.get("/summery",response_model=DashboardSummary)
def dashboard_summry(db:Session=Depends(get_db)):
    return DashboardService.get_summery(db)

@router.get("/priority",response_model=List[PriorityStatistics])
def priority_dashboard(db:Session=Depends(get_db)):
    return DashboardService.priority_statistics(db)


@router.get("/category",response_model=List[CategoryStatistics])
def priority_dashboard(db:Session=Depends(get_db)):
    return DashboardService.category_statistics(db)

@router.get("/agent-performance",response_model=List[AgentPerformance])
def priority_dashboard(db:Session=Depends(get_db)):
    return DashboardService.agent_performance(db)

