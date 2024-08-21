from api.user.user_model import User
from api.user.dto import CreateUserDTO
from api.user.strategies import CreateUserStrategy


class DefaultCreateUserStrategy(CreateUserStrategy):
    @staticmethod
    async def create_user(user: CreateUserDTO):
        return await User.create_default_user(
            user.name, user.email, user.password, user.roles
        )
