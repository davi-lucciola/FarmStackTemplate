from fastapi import HTTPException, status
import datetime as dt
from api.utils import jwt
from api.auth.strategies import (
    LoginStrategy,
    LoginStrategies,
    DefaultLoginStrategy,
    GoogleLoginStrategy,
)
from api.config import settings
from api.auth.dto import LoginDTO
from api.user.user_model import User
from jose.exceptions import ExpiredSignatureError, JWTError

from api.utils.logger import ilogger


login_strategies: dict[LoginStrategies, LoginStrategy] = {
    LoginStrategies.DEFAULT: DefaultLoginStrategy,
    LoginStrategies.GOOGLE: GoogleLoginStrategy,
}


async def login(
    credentials: LoginDTO, strategy: LoginStrategies
) -> str:
    token: str = await login_strategies.get(strategy).login(credentials)
    return token


def create_token(user_id: object) -> str:
    initiated_at: dt.datetime = dt.datetime.now()
    expires_on: dt.datetime = dt.datetime.now() + dt.timedelta(
        seconds=settings.EXPIRATION_SECONDS
    )

    token_payload = {"exp": expires_on, "iat": initiated_at, "sub": str(user_id)}

    access_token: str = jwt.encode_token(token_payload)
    return access_token


async def authenticate(token: str) -> User:
    try:
        payload: dict = jwt.decode_token(token)
    except ExpiredSignatureError:
        raise HTTPException(
            detail='Token Expirado.', 
            status_code=status.HTTP_403_FORBIDDEN
        )
    except JWTError:
        raise HTTPException(
            detail='Token inválido.', 
            status_code=status.HTTP_403_FORBIDDEN
        )
    
    user = await User.get(payload.get("sub"))

    if user is None:
        raise HTTPException(
            detail='Usuário não encontrado.', 
            status_code=status.HTTP_403_FORBIDDEN
        )

    return user
