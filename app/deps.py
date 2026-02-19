from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.auth import verify_token


security = HTTPBearer()


def get_user(

    credentials: HTTPAuthorizationCredentials = Depends(security)

):

    token = credentials.credentials

    user_id = verify_token(token)


    if user_id is None:

        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )


    return user_id
