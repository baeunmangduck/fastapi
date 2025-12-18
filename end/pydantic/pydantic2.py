from pydantic import BaseModel, ConfigDict, Field, Strict, ValidationError
from typing import List, Annotated


class Address(BaseModel):
    street: str
    city: str
    country: str


class User(BaseModel):
    # 전체 요소에서 str -> int로 자동 파싱하는 기능을 원하지 않을 경우 아래의 코드 사용
    # model_config = ConfigDict(strict=True)

    id: int
    name: str
    email: str
    addresses: List[Address]

    age: int | None = None
    # age: int = Field(None, strict=True)
    # age: Annotated[int, Strict()] = None
    # 하나의 요소만 데이터 타입 자동 파싱을 방지하고 싶을 경우 


# Pydantic Model 객체화 시 자동으로 검증 수행 수행하고, 검증 오류 시 ValidationError raise
try:
    user = User(
        id="3",
        name="John Doe",
        email="john.doe@example.com",
        addresses=[{"street": "123 Main St", "city": "Hometown", "country": "USA"}],
        age="29",  # 문자열 값을 자동으로 int 로 파싱 가능한 경우 존재
    )
    print(user)
except ValidationError as e:
    print("validation error happened")
    print(e)
