from typing import TypedDict


class UserMetaDTO(TypedDict):
    name: str
    avatar_path: str
    time_block: int


class UserDTO(TypedDict):
    meta: UserMetaDTO
    login: str
