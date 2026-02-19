from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import sys
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from app.database import get_db
from app.deps import get_user

from app.models import ChatHistory, UsageTracking

from app.rag import ask_question


router = APIRouter()


@router.post("/chat")
def chat(
    query: str,
    user_id: int = Depends(get_user),
    db: Session = Depends(get_db)
):

    # get AI response
    response = ask_question(user_id, query)


    # save chat history
    chat = ChatHistory(
        user_id=user_id,
        query=query,
        response=response
    )

    db.add(chat)


    # count tokens (simple method)
    tokens = len(query.split()) + len(response.split())


    # update usage tracking
    usage = db.query(UsageTracking).filter(
        UsageTracking.user_id == user_id
    ).first()


    if usage:

        usage.query_count += 1

        usage.token_usage += tokens

    else:

        usage = UsageTracking(
            user_id=user_id,
            query_count=1,
            token_usage=tokens
        )

        db.add(usage)


    db.commit()


    return {

        "response": response

    }
