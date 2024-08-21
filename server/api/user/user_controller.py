from typing import List
from fastapi import APIRouter, Depends
from api.utils import BasicResponse
from api.user import user_service
from api.user.dto import UserDTO, CreateUserDTO, UpdateUserDTO
from api.user.strategies import CreateUserStrategies
from api.user.user_model import User
from api.auth.authorization import Roles
from api.auth.guard import AuthGuard, PermissionGuard


user_router = APIRouter(prefix="/users", tags=["User"])


@user_router.post("/signup")
async def signup(user_dto: CreateUserDTO):
    await user_service.create(user_dto, CreateUserStrategies.DEFAULT)
    return BasicResponse(detail="Usuário cadastrado com sucesso.")


@user_router.get("/", dependencies=[Depends(AuthGuard(Roles.ADMIN))])
async def get_all_users() -> List[UserDTO]:
    return await user_service.find_all()


@user_router.get("/{id}", dependencies=[Depends(PermissionGuard(Roles.ADMIN, User))])
async def get_user_by_id(id: str) -> UserDTO:
    return await user_service.find_by_id(id)


@user_router.post("/")
async def create_user(
    user_dto: CreateUserDTO, user: User = Depends(AuthGuard(Roles.ADMIN))
):
    await user_service.create(user_dto, CreateUserStrategies.DEFAULT, user.roles)
    return BasicResponse(detail="Usuário cadastrado com sucesso.")


@user_router.put("/{id}")
async def update_user(
    id: str,
    user_dto: UpdateUserDTO,
    user: User = Depends(PermissionGuard(Roles.ADMIN, User)),
):
    await user_service.update(id, user_dto, user.roles)
    return BasicResponse(detail="Usuário atualizado com sucesso.")


@user_router.delete("/{id}", dependencies=[Depends(PermissionGuard(Roles.ADMIN, User))])
async def delete_user(id: str):
    await user_service.delete(id)
    return BasicResponse(detail="Usuário excluído com sucesso.")
