from api.utils import crypt
from typing import Optional, Annotated
from beanie import Document, Indexed, PydanticObjectId


class User(Document):
    name: str
    email: Annotated[str, Indexed(unique=True)]
    password: Optional[str] = None
    profile_picture_uri: Optional[str] = None
    fl_google_user: bool = False

    def check_password(self, plain_password: str) -> bool:
        return crypt.check_hash(plain_password, self.password)

    @staticmethod
    async def get_by_email(email: str) -> Optional["User"]:
        return await User.find(User.email == email).first_or_none()

    @staticmethod
    async def create_default_user(name: str, email: str, password: str):
        user = User(name=name, email=email, password=crypt.hash(password))

        await user.save()
        return user

    @staticmethod
    async def create_google_user(name: str, email: str, profile_picture_uri: str):
        user = User(name=name, email=email, profile_picture_uri=profile_picture_uri)

        user.password = None
        user.fl_google_user = True

        await user.save()

        return user

    def __repr__(self) -> str:
        return f"<User - {self.name}>"

    def __str__(self) -> str:
        return f"<User - {self.name}>"

    class Settings:
        name = "users"
