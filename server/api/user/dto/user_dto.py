from typing import Optional, List
from beanie import PydanticObjectId as OID
from pydantic import BaseModel
from api.auth.authorization import Roles


class UserDTO(BaseModel):
    id: OID
    name: str
    email: str
    roles: List[Roles]
    profile_picture_uri: Optional[str]
    fl_google_user: bool

    class Config:
        from_attributes = True
