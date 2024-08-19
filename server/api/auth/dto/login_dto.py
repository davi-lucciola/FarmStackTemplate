from pydantic import BaseModel, field_validator
from api.utils.validators import email_validator


class LoginDTO(BaseModel):
    email: str
    password: str

    @field_validator("email")
    def email_validation(cls, value: str | None) -> str:
        return email_validator(value)
