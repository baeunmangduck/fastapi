from pydantic import BaseModel, Field, ValidationError
from typing import Optional


# ----------------------------------------
# User Model 예시 (Field Example 포함)
# ----------------------------------------
class User(BaseModel):
    username: str = Field(
        ...,
        description="user name",
        json_schema_extra={"example": "john_doe"},  # Swagger 예제 표시용
    )
    email: str = Field(
        ...,
        description="email address",
        json_schema_extra={"example": "aaa@example.com"},
    )
    password: str = Field(
        ...,
        min_length=8,  # 비밀번호 최소 길이
        description="user password",
        json_schema_extra={"example": "Secret123"},
    )
    age: Optional[int] = Field(
        None,
        ge=0,  # 나이 최소 = 0
        le=120,  # 나이 최대 = 120
        description="user age (0 ~ 120)",
        json_schema_extra={"example": 30},
    )
    is_active: bool = Field(
        True, description="currently active?", json_schema_extra={"example": True}
    )


# ----------------------------------------
# Validation 테스트
# ----------------------------------------
try:
    user = User(
        username="john_doe",
        email="john.doe@example.com",
        password="Set33123",
        is_active=0,  # bool이므로 0 → False 로 자동 변환
    )
    print(user)
except ValidationError as e:
    print(e.json())


# ============================================================
#               숫자 검증 옵션 예제 (gt, ge, lt, le 등)
# ============================================================

"""
gt  : greater than (초과)
ge  : greater than or equal (이상)
lt  : less than (미만)
le  : less than or equal (이하)
multiple_of : 특정 숫자의 배수
allow_inf_nan : inf, -inf, nan 허용 여부
"""


class Foo(BaseModel):
    positive: int = Field(gt=0)  # 0보다 큰 값
    non_negative: int = Field(ge=0)  # 0 이상
    negative: int = Field(lt=0)  # 0 미만
    non_positive: int = Field(le=0)  # 0 이하
    even: int = Field(multiple_of=2)  # 짝수만 허용
    special: float = Field(allow_inf_nan=True)  # inf, -inf, nan 허용


foo = Foo(
    positive=1,
    non_negative=0,
    negative=-1,
    non_positive=0,
    even=4,
    special=float("inf"),
)
print(foo)


# ============================================================
#               문자열 검증 옵션 예제
# ============================================================

"""
min_length : 최소 길이
max_length : 최대 길이
pattern    : 정규표현식(regex) 패턴 검사
"""


class Foo(BaseModel):
    short: str = Field(min_length=3)  # 최소 3글자
    long: str = Field(max_length=10)  # 최대 10글자
    numeric_only: str = Field(pattern=r"^\d+$")  # 숫자만 허용


foo = Foo(short="abc", long="abcdefgh", numeric_only="12345")
print(foo)


# ============================================================
#               Decimal 정밀도 검증(max_digits, decimal_places)
# ============================================================

"""
max_digits     : 전체 자릿수 제한 (소수 포함)
decimal_places : 소수점 이하 자리수 제한
"""

from decimal import Decimal


class Foo(BaseModel):
    precise: Decimal = Field(
        max_digits=6, decimal_places=2  # 전체 6자리까지 가능  # 소수점 이하 2자리까지
    )


# OK
foo = Foo(precise=Decimal("1234.56"))
print(foo)

# 실패 예시 (전체 자릿수 초과)
# Foo(precise=Decimal("123456.78"))  # max_digits 초과 → ValidationError

# 실패 예시 (소수점 자리 초과)
# Foo(precise=Decimal("12.345"))     # decimal_places 초과 → ValidationError
