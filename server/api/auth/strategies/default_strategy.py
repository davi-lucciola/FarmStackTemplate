from fastapi import HTTPException, status
from api.user.user_model import User
from api.auth import auth_service
from api.auth.dto import LoginDTO
from api.auth.strategies import LoginStrategy


class DefaultLoginStrategy(LoginStrategy):
    @staticmethod
    async def login(credentials: LoginDTO) -> str:
        user = await User.get_by_email(credentials.email)

        if user is not None and user.fl_google_user is True and user.password is None:
            raise HTTPException(
                detail="Usuário associado a uma conta google sem senha cadastrada. Entre com o google.",
                status_code=status.HTTP_401_UNAUTHORIZED,
            )

        if user is None or user.check_password(credentials.password) is False:
            raise HTTPException(
                detail="Credenciais Inválidas.",
                status_code=status.HTTP_401_UNAUTHORIZED,
            )

        access_token = auth_service.create_token(user.id)
        return access_token
