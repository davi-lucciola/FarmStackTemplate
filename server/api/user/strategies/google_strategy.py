from api.user.user_model import User
from api.user.dto import CreateUserDTO
from api.user.strategies import CreateUserStrategy


class GoogleCreateUserStrategy(CreateUserStrategy):
    @staticmethod
    async def create_user(user: CreateUserDTO):
        return await User.create_google_user(
            user.name, user.email, user.profile_picture_uri
        )
