from typing import Optional
from beanie import PydanticObjectId as OID
from pydantic import BaseModel



class UserDTO(BaseModel):
    id: OID
    email: str
    name: str
    profile_picture_uri: Optional[str]
    fl_google_user: bool

    class Config:
        from_attributes = True