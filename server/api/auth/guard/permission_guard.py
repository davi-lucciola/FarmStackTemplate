from dataclasses import dataclass
from typing import List, Optional
from fastapi import Security, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from api.auth import SECURITY_BEARER
from api.auth.guard import AuthGuard
from api.auth.authorization import Roles
from api.user.user_model import User
from api.utils.models import IDocument


@dataclass
class PermissionGuard(AuthGuard):
    """Guard to be used with FastAPI "Depends" to authorizate
    if the user have one of the roles or he is the owner of the resource


    Args:
        roles (List[Roles] | Roles | None):
            - Roles that the user must have
        document (IDocument | None):
            - Document to validate if the user are the owner of the resource

    Raises:
        HTTPException: Unauthorized and Forbidden HTTPException responses
    """

    roles: List[Roles] | Roles | None = None
    document: Optional[IDocument] = None

    async def __call__(
        self,
        id: str,
        auth: Optional[HTTPAuthorizationCredentials] = Security(SECURITY_BEARER),
    ) -> User:
        user: User = await self.validate_auth(auth)

        if (
            user.authorize(self.roles) is False
            and await user.can_update(id, str(user.id)) is False
        ):
            raise HTTPException(
                detail="Usuário não autorizado.", status_code=status.HTTP_403_FORBIDDEN
            )

        return user

    def __hash__(self) -> int:
        return hash((type(self),))
