from jose import jwt, JWTError
from datetime import datetime, timedelta

SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"
EXPIRATION_MINUTES = 60


def create_token(user_id: int):

    payload = {

        "user_id": user_id,

        "exp": datetime.utcnow() + timedelta(minutes=EXPIRATION_MINUTES)
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return token


def verify_token(token: str):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload["user_id"]

    except JWTError:

        return None
