from dataclasses import dataclass
from fastapi import Security, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from api.auth import auth_service
from api.auth import SECURITY_BEARER
from api.user.user_model import User


@dataclass
class AuthGuard:
    async def __call__(self, 
        auth: HTTPAuthorizationCredentials | None = Security(SECURITY_BEARER)
    ) -> User:
        if auth is None:
            raise HTTPException(
                detail="Usuário não autenticado.", 
                status_code=status.HTTP_403_FORBIDDEN
            )

        return await auth_service.authenticate(auth.credentials)
    
    def __hash__(self) -> int:
        return hash((type(self),))