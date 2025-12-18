from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    HttpUrl,
    AnyHttpUrl,
    AnyUrl,
    FileUrl,
    IPvAnyAddress,
    IPvAnyInterface,
    IPvAnyNetwork,
)

# Email 문자열 검증
# EmailStr → 실제 이메일 형식 검증 (email-validator 패키지 필요)
# Field(pattern=...) → 추가적인 정규식 검증도 동시에 가능
# max_length → 이메일 길이 제한
class UserEmail(BaseModel):
    email: EmailStr = Field(
        None,
        max_length=40,
        pattern=r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$",
    )


try:
    user_email = UserEmail(email="aaa@example.com")
    print(user_email)
except ValueError as e:
    print(e)


# URL 관련 자료형 검증
class UserResource(BaseModel):
    # HttpUrl → 반드시 http:// 또는 https:// 이어야 함
    http_url: HttpUrl

    # AnyHttpUrl → HttpUrl과 동일하지만, 도메인 제약이 더 느슨함
    any_http_url: AnyHttpUrl

    # AnyUrl → http, https, ftp, ws 등 어떤 스킴(프로토콜)이든 허용
    # 예: ftp://example.com, ws://localhost
    any_url: AnyUrl

    # FileUrl → 반드시 file:// 로 시작하는 로컬 파일 경로
    file_url: FileUrl


try:
    user_resource = UserResource(
        http_url="https://www.example.com",
        any_http_url="http://www.bbb.com",
        any_url="ftp://example.com",      # : 이 반드시 있어야 함
        file_url="file://path/to/file.log",
    )
    print(user_resource)
except ValueError as e:
    print(e)


# IP 주소 관련 검증 타입
class IP_Address(BaseModel):
    # IPvAnyAddress → IPv4 또는 IPv6 주소 모두 허용
    address: IPvAnyAddress

    # IPvAnyInterface → IP + Mask 형태의 표기 검증
    # 예: "192.168.0.1/24" 또는 "2001:db8::/32"
    interface: IPvAnyInterface

    # IPvAnyNetwork → 네트워크 주소 검증 (prefix 기반)
    # 예: "192.168.0.0/16" 또는 "2001:db8::/32"
    network: IPvAnyNetwork


try:
    ip_data = IP_Address(
        address="192.168.0.1",
        interface="192.168.0.1/24",
        network="192.168.0.0/16",
    )
    print(ip_data)
except ValueError as e:
    print(e)


# 국가 코드 검증 (pydantic-extra-types 필요)
# pip install pydantic-extra_types / pip install pycountry 설치 필요
from pydantic_extra_types.country import CountryAlpha3


class Country(BaseModel):
    # ISO ALPHA-3 국가 코드 검증 (USA, KOR, JPN 등 3자리 표준)
    made_in: CountryAlpha3


try:
    country = Country(made_in="KOR")
    print(country)
except ValueError as e:
    print(e)