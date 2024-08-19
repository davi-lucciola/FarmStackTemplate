from enum import Enum, auto
from abc import ABC, abstractmethod
from api.user.dto import CreateUserDTO
from api.user.user_model import User


class CreateUserStrategy(ABC):
    @staticmethod
    @abstractmethod
    async def create_user(user: CreateUserDTO) -> User:
        raise NotImplementedError("Create User Not Implemented")


class CreateUserStrategies(Enum):
    DEFAULT = auto()
    GOOGLE = auto()


from .default_strategy import DefaultCreateUserStrategy
from .google_strategy import GoogleCreateUserStrategy
