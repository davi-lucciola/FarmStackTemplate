from typing import List
from fastapi import HTTPException, status
from api.user.strategies import (
    CreateUserStrategies,
    CreateUserStrategy,
    DefaultCreateUserStrategy,
    GoogleCreateUserStrategy,
)
from api.user.user_model import User
from api.user.dto import CreateUserDTO, UpdateUserDTO
from api.auth.authorization import Roles


create_user_strategies: dict[CreateUserStrategies, CreateUserStrategy] = {
    CreateUserStrategies.DEFAULT: DefaultCreateUserStrategy,
    CreateUserStrategies.GOOGLE: GoogleCreateUserStrategy,
}


async def find_all() -> List[User]:
    return await User.find_all().to_list()


async def find_by_id(user_id: str) -> User:
    user = await User.get(user_id)

    if user is None:
        raise HTTPException(
            detail="Usuário não encontrado.", status_code=status.HTTP_404_NOT_FOUND
        )

    return user


async def create(
    user_dto: CreateUserDTO,
    strategy: CreateUserStrategies,
    agent_roles: List[Roles] = [],
):
    if Roles.ADMIN in user_dto.roles and Roles.ADMIN not in agent_roles:
        raise HTTPException(
            detail="Você não tem permissão para cadastrar um usuário ADMIN.",
            status_code=status.HTTP_403_FORBIDDEN,
        )

    exist_user = await User.get_by_email(user_dto.email)

    if exist_user is not None:
        raise HTTPException(
            detail="Usuário já cadastrado com esse email.",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    new_user = await create_user_strategies.get(strategy).create_user(user_dto)
    return new_user


async def update(user_id: str, user_dto: UpdateUserDTO, agent_roles: List[Roles] = []):
    if Roles.ADMIN in user_dto.roles and Roles.ADMIN not in agent_roles:
        raise HTTPException(
            detail="Você não tem permissão para tornar um usuário ADMIN.",
            status_code=status.HTTP_403_FORBIDDEN,
        )

    user_to_update = await find_by_id(user_id)

    if user_to_update.fl_google_user is False and user_dto.password is None:
        raise HTTPException(
            detail="Você precisa passar uma senha para um usuário de sistema.",
            status_code=status.HTTP_400_BAD_REQUEST
        )

    update_email_google_user = (
        user_to_update.fl_google_user is True and user_dto.email != user_to_update.email
    )

    if update_email_google_user:
        if user_dto.password is None:
            raise HTTPException(
                detail="Você precisa inserir uma senha ao editar o email de um usuário google. A autenticação pelo google também não será mais possivel.",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        user_to_update.fl_google_user = False

    email_already_register = (
        await User.find(User.email == user_dto.email)
        .find(User.id != user_to_update.id)
        .first_or_none()
        is not None
    )

    if email_already_register:
        raise HTTPException(
            detail="Usuário já cadastrado com esse email.",
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    
    user_to_update.fill(user_dto)
    await user_to_update.save()
    
    return user_to_update


async def delete(user_id: str):
    user_to_delete = await find_by_id(user_id)
    await user_to_delete.delete()
