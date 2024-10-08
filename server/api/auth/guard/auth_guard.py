from dataclasses import dataclass
from typing import List, Optional
from fastapi import Security, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from api.auth import auth_service
from api.auth import SECURITY_BEARER
from api.auth.authorization import Roles
from api.user.user_model import User


@dataclass
class AuthGuard:
    """Guard to be used with FastAPI "Depends" to authorizate
    if the user have one of the roles


    Args:
        roles (List[Roles] | Roles | None):
            - Roles that the user must have

    Raises:
        HTTPException: Unauthorized and Forbidden HTTPException responses
    """

    roles: List[Roles] | Roles | None = None

    async def __call__(
        self, auth: Optional[HTTPAuthorizationCredentials] = Security(SECURITY_BEARER)
    ) -> User:
        user = await self.validate_auth(auth)

        if user.authorize(self.roles) is False:
            raise HTTPException(
                detail="Usuário não autorizado.", status_code=status.HTTP_403_FORBIDDEN
            )

        return user

    async def validate_auth(self, auth: Optional[HTTPAuthorizationCredentials]) -> User:
        if auth is None:
            raise HTTPException(
                detail="Usuário não autenticado.",
                status_code=status.HTTP_401_UNAUTHORIZED,
            )

        user = await auth_service.authenticate(auth.credentials)
        return user

    def __hash__(self) -> int:
        return hash((type(self),))
