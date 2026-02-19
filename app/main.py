from fastapi import FastAPI
import sys
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from app.routes.auth_routes import router as auth_router
from app.routes.upload_routes import router as upload_router
from app.routes.chat_routes import router as chat_router
from app.routes.history_routes import router as history_router


app = FastAPI()


@app.get("/")
def home():

    return {

        "status": "running"
    }


app.include_router(auth_router)

app.include_router(upload_router)

app.include_router(chat_router)

app.include_router(history_router)
