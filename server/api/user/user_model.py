from typing import List
from typing import Optional, Annotated
from beanie import Indexed
from api.utils import crypt
from api.utils.models import IDocument
from api.auth.authorization import Roles
from api.user.dto import UpdateUserDTO


class User(IDocument):
    name: str
    email: Annotated[str, Indexed(unique=True)]
    password: Optional[str] = None
    roles: List[Roles] = [Roles.USER]
    fl_google_user: bool = False
    profile_picture_uri: Optional[str] = None

    def check_password(self, plain_password: str) -> bool:
        return crypt.check_hash(plain_password, self.password)

    def authorize(self, roles: List[Roles] | Roles | None) -> bool:
        if roles is None:
            return True
        elif isinstance(roles, str) and roles in self.roles:
            return True
        elif isinstance(roles, list):
            for role in roles:
                if role in self.roles:
                    return True

        return False

    def fill(self, user_dto: UpdateUserDTO) -> None:
        self.name = user_dto.name
        self.email = user_dto.email
        self.password = crypt.hash(user_dto.password) if user_dto.password is not None else None
        self.profile_picture_uri = user_dto.profile_picture_uri
        self.roles = user_dto.roles if len(user_dto.roles) != 0 else [Roles.USER]

    @classmethod
    async def get_by_email(cls, email: str) -> Optional["User"]:
        return await cls.find(User.email == email).first_or_none()

    @classmethod
    async def create_default_user(
        cls, name: str, email: str, password: str, roles: Optional[List[Roles]]
    ):
        if roles is None or len(roles) == 0:
            roles = [Roles.USER]
        user = User(name=name, email=email, password=crypt.hash(password), roles=roles)

        await user.save()
        return user

    @classmethod
    async def create_google_user(cls, name: str, email: str, profile_picture_uri: str):
        user = User(name=name, email=email, profile_picture_uri=profile_picture_uri)

        user.password = None
        user.fl_google_user = True
        user.roles = [Roles.USER]

        await user.save()

        return user

    @classmethod
    async def can_update(
        cls, resource_id: Optional[str], user_id: Optional[str]
    ) -> bool:
        if resource_id is None:
            return True

        user_to_update = await User.get(resource_id)
        if user_to_update is None or str(user_to_update.id) == user_id:
            return True

        return False

    def __str__(self) -> str:
        return f"<User ({self.id}) - {self.name}>"

    class Settings:
        name = "users"
