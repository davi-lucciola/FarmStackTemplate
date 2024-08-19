from typing import List, Optional
from fastapi import HTTPException, status
from api.user.strategies import (
    CreateUserStrategies,
    CreateUserStrategy,
    DefaultCreateUserStrategy,
    GoogleCreateUserStrategy,
)
from api.user.user_model import User
from api.user.dto import CreateUserDTO


create_user_strategies: dict[CreateUserStrategies, CreateUserStrategy] = {
    CreateUserStrategies.DEFAULT: DefaultCreateUserStrategy,
    CreateUserStrategies.GOOGLE: GoogleCreateUserStrategy,
}


async def find_all() -> List[User]:
    return await User.find_all().to_list()


async def find_by_id(document_id: str) -> Optional[User]:
    return await User.get(document_id)

async def create(user: CreateUserDTO, strategy: CreateUserStrategies):
    exist_user = await User.get_by_email(user.email)

    if exist_user is not None:
        raise HTTPException(
            detail="Usuário já cadastrado com esse email.",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    new_user = await create_user_strategies.get(strategy).create_user(user)
    return new_user
