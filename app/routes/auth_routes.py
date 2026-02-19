from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import sys
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from app.database import get_db
from app.models import User
from app.auth import create_token

router = APIRouter()


# Register
@router.post("/register")
def register(

    email: str,

    password: str,

    db: Session = Depends(get_db)

):

    existing = db.query(User).filter(

        User.email == email

    ).first()


    if existing:

        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )


    user = User(

        email=email,

        password=password
    )


    db.add(user)

    db.commit()

    db.refresh(user)


    return {

        "message": "Registered successfully"
    }


# Login
@router.post("/login")
def login(

    email: str,

    password: str,

    db: Session = Depends(get_db)

):

    user = db.query(User).filter(

        User.email == email,

        User.password == password

    ).first()


    if not user:

        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )


    token = create_token(user.id)


    return {

        "access_token": token,

        "token_type": "bearer"

    }
