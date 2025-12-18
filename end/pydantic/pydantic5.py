from pydantic import BaseModel, ValidationError, field_validator, model_validator
from typing import Optional


class User(BaseModel):
    username: str
    password: str
    confirm_password: str

    @field_validator("username")
    def username_not_empty(cls, value: str):
        if not value.strip():
            return ValueError("Username must not be empty")
        return value

    @field_validator("password")
    def password_validation(cls, value: str):
        if len(value) < 10:
            raise ValueError("Password must be at least 10 characters long")

        if not any(char.isdigit() for char in value):
            raise ValueError("Password must contain at least one digit")

        if not any(char.isalpha() for char in value):
            raise ValueError("Password must contain at least one letter")

        return value

    @model_validator(mode="after")
    def check_password_match(self):
        pwd = self.password
        confirm_password = self.confirm_password
        if pwd != confirm_password:
            raise ValueError("Password not match")
        return self


try:
    user = User(
        username="baeunmangduck", password="hello12345", confirm_password="hello12345"
    )
    print(user)
except ValidationError as e:
    print(e)
