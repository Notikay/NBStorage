from typing import TypedDict


class SettingsDTO(TypedDict):
    name: str
    avatar_path: str
    time_block: int


class UserDTO(TypedDict):
    settings: SettingsDTO
    login: str
