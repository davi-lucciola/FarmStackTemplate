from typing import Optional
from pydantic import BaseModel, field_validator
from api.utils.validators import email_validator


class CreateUserDTO(BaseModel):
    name: str
    email: str
    password: str
    profile_picture_uri: Optional[str] = None

    @field_validator("email")
    def email_validation(cls, value: str) -> str:
        value = email_validator(value)
        return value
