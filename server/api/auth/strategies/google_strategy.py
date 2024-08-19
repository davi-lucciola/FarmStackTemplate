import httpx
from fastapi import HTTPException, status
from api.config import settings
from api.user import user_service
from api.user.user_model import User
from api.user.dto import CreateUserDTO
from api.auth import auth_service
from api.auth.dto import LoginDTO, GoogleUserDTO
from api.user.strategies import CreateUserStrategies
from api.auth.strategies import LoginStrategy


class GoogleLoginStrategy(LoginStrategy):
    @staticmethod
    async def login(credentials: LoginDTO) -> str:
        user_info = GoogleLoginStrategy.get_google_user_info(
            credentials.password
        )

        user = await User.get_by_email(user_info["email"])

        if user is None:
            create_user_dto = CreateUserDTO(
                name=user_info["name"],
                email=user_info["email"],
                password="",
                profile_picture_uri=user_info["picture"],
            )

            user = await user_service.create(
                create_user_dto, CreateUserStrategies.GOOGLE
            )

        if user.fl_google_user is False:
            raise HTTPException(
                detail="Usuário não vinculado a uma conta google, entre com suas credenciais de sistema.",
                status_code=status.HTTP_401_UNAUTHORIZED,
            )

        return auth_service.create_token(user.id)

    @staticmethod
    def get_google_user_info(code: str) -> GoogleUserDTO:
        token_url = "https://accounts.google.com/o/oauth2/token"

        data = {
            "code": code,
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "redirect_uri": settings.GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code",
        }

        response = httpx.post(token_url, data=data)

        if response.is_error:
            raise HTTPException(
                detail="Erro ao consultar token do google.",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        access_token = response.json().get("access_token")

        response = httpx.get(
            "https://www.googleapis.com/oauth2/v1/userinfo",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        if response.is_error:
            raise HTTPException(
                detail="Erro ao consultar informações do usuário google.",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return response.json()
