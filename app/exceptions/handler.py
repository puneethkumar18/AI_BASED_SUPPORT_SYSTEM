from fastapi import Request
from fastapi.responses import JSONResponse
from app.exceptions.custom_exception import *

async def ticket_not_found_handler(
    request: Request,
    exc: TicketNotFoundException):

    return JSONResponse(
        status_code=404,
        content={
            "success": False,
            "message": exc.message
        }
    )


async def user_not_found_handler(request:Request,exc:UserNotFoundException):
    return JSONResponse(
        status_code=404,
        content={
            "success":False,
            "message":exc.exc.message
        }
    )


async def knowledge_not_found_handler(request:Request,exc:KnowledgeNotFoundException):
    return JSONResponse(
        status_code=404,
        content={
            "success":False,
            "message":exc.exc.message
        }
    )
