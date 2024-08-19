from typing import List
from fastapi import APIRouter, Depends
from api.user import user_service
from api.user.dto import CreateUserDTO
from api.user.strategies import CreateUserStrategies
from api.utils import BasicResponse
from api.user.dto import UserDTO
from api.auth.guard import AuthGuard


user_router = APIRouter(prefix="/users", tags=["User"])


@user_router.get("/", dependencies=[Depends(AuthGuard())])
async def get_all_users() -> List[UserDTO]:
    return await user_service.find_all()


@user_router.get("/{id}")
async def get_user_by_id(id: str) -> UserDTO:
    return await user_service.find_by_id(id)


@user_router.post("/")
async def create_new_user(user_dto: CreateUserDTO):
    await user_service.create(user_dto, CreateUserStrategies.DEFAULT)
    return BasicResponse(detail="Usuário cadastrado com sucesso.")
