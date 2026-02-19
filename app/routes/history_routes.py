from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_user
from app.models import ChatHistory


router = APIRouter()


@router.get("/history")
def get_history(
    user_id: int = Depends(get_user),
    db: Session = Depends(get_db)
):

    chats = db.query(ChatHistory).filter(
        ChatHistory.user_id == user_id
    ).all()


    # convert to JSON manually
    history = []

    for chat in chats:

        history.append({

            "id": chat.id,

            "query": chat.query,

            "response": chat.response,

            "created_at": str(chat.created_at)

        })


    return {

        "user_id": user_id,

        "history": history

    }
