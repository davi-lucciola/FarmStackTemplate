from enum import Enum, auto
from abc import ABC, abstractmethod
from api.auth.dto import LoginDTO


class LoginStrategy(ABC):
    @staticmethod
    @abstractmethod
    async def login(credentials: LoginDTO) -> str:
        raise NotImplementedError("Login Method Not Implemented")


class LoginStrategies(Enum):
    DEFAULT = auto()
    GOOGLE = auto()


from .default_strategy import DefaultLoginStrategy
from .google_strategy import GoogleLoginStrategy
