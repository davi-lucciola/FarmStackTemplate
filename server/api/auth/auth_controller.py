from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from api.config import settings
from api.auth import auth_service
from api.auth.dto import LoginDTO
from api.auth.strategies import LoginStrategies


auth_router = APIRouter(prefix="/auth", tags=["Authentication"])


@auth_router.get("/google/login")
async def login_google():
    uri = (
        "https://accounts.google.com/o/oauth2/v2/auth?"
        + f"response_type=code&client_id={settings.GOOGLE_CLIENT_ID}&"
        + f"redirect_uri={settings.GOOGLE_REDIRECT_URI}&"
        + "scope=openid%20profile%20email&access_type=offline"
    )
    return RedirectResponse(uri)


# @auth_router.get("/login/google")
# async def login_google():
#     return {
#         "uri": f"https://accounts.google.com/o/oauth2/v2/auth?response_type=code&client_id={settings.GOOGLE_CLIENT_ID}&redirect_uri={settings.GOOGLE_REDIRECT_URI}&scope=openid%20profile%20email&access_type=offline"
#     }


@auth_router.get("/google/token")
async def auth_google(code: str):
    credentials = LoginDTO(email="notmatter@email.com", password=code)
    token: str = await auth_service.login(
        credentials, LoginStrategies.GOOGLE
    )
    return {"access_token": token, "type": "bearer"}


@auth_router.post("/default/token")
async def auth_default(credentials: LoginDTO):
    token: str = await auth_service.login(
        credentials, LoginStrategies.DEFAULT
    )
    return {"access_token": token, "type": "bearer"}
