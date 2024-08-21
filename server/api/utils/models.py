from abc import ABC, abstractmethod
from typing import Optional
from beanie import Document
from pydantic import BaseModel


class BasicResponse(BaseModel):
    detail: str


class IDocument(Document, ABC):
    @classmethod
    @abstractmethod
    async def can_update(
        cls, resource_id: Optional[str], user_id: Optional[str]
    ) -> bool:
        raise NotImplementedError("Can Update Method not implemented.")