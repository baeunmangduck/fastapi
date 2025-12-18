from pydantic import BaseModel
import json


class User(BaseModel):
    id: int
    name: str
    email: str
    age: int | None = None


class UserClass:
    def __init__(self, id: int, name: str, email: str, age: int):
        self.id = id
        self.name = name
        self.email = email
        self.age = age

    def get_info(self):
        return f"id: {self.id}, name: {self.name}"

    def __str__(self):
        return (
            f"id: {self.id}, name: {self.name}, "
            f"email: {self.email}, age: {self.age}"
        )


# 1) 일반 클래스 사용
user_obj = UserClass(1, "alice", "alice@example.com", 25)
print("user_obj:", user_obj)
print("user_obj id:", user_obj.id)

# 2) Pydantic 모델 직접 생성
user = User(id=2, name="bob", email="bob@example.com", age=30)
print("user:", user)
print("user id:", user.id)

# 3) dict → Pydantic 모델
user_data = {
    "id": 3,
    "name": "charlie",
    "email": "charlie@example.com",
    "age": 28,
}
user_from_dict = User(**user_data)
print("user_from_dict:", user_from_dict, user_from_dict.id)

# 4) JSON 문자열 → Pydantic 모델
json_string = """
{
  "id": 4,
  "name": "diana",
  "email": "diana@example.com",
  "age": 32
}
"""
json_dict = json.loads(json_string)
user_from_json = User(**json_dict)
print("user_from_json:", user_from_json, user_from_json.id)


# 5) 상속 모델
class AdvancedUser(User):
    level: int


adv_user = AdvancedUser(
    id=5,
    name="eric",
    email="eric@example.com",
    age=35,
    level=10,
)
print("adv_user:", adv_user)


# 6) Nested 모델
class Address(BaseModel):
    street: str
    city: str


class UserNested(BaseModel):
    name: str
    age: int
    address: Address


json_string_nested = """
{
  "name": "frank",
  "age": 29,
  "address": {
    "street": "456 River Rd",
    "city": "Seoul"
  }
}
"""
json_dict_nested = json.loads(json_string_nested)
user_nested_01 = UserNested(**json_dict_nested)
print(
    "user_nested_01:",
    user_nested_01,
    user_nested_01.address,
    user_nested_01.address.city,
)

user_nested_02 = UserNested(
    name="gina",
    age=27,
    address={"street": "789 Ocean Ave", "city": "Busan"},
)
print(
    "user_nested_02:",
    user_nested_02,
    user_nested_02.address,
    user_nested_02.address.city,
)

# 7) 직렬화
user_dump_01 = user.model_dump()
print("user_dump_01:", user_dump_01, type(user_dump_01))

user_dump_02 = user.model_dump_json()
print("user_dump_02:", user_dump_02, type(user_dump_02))
