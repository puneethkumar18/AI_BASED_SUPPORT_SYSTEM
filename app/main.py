from fastapi import FastAPI
from app.database.database import engine

from app.routers.auth import router as auth_router
from app .routers.ticket import router as ticket_router
from app.routers.knowledge import router as knowledge_router
from app.routers.comment import router as comment_router
from app.routers.user import router as user_router
from app.routers.history import router as history_router



app = FastAPI()

app.include_router(user_router)
app.include_router(auth_router)
app.include_router(ticket_router)
app.include_router(knowledge_router)
app.include_router(comment_router)
app.include_router(history_router)



@app.get("/")
def home():
    connection = engine.connect()
    connection.close()

    return {
        "message": "Database Connected Successfully"
    }


@app.get("/db-test")
def db_test():
    conn = engine.connect()
    conn.close()
    return {"message": "DB Connected"}