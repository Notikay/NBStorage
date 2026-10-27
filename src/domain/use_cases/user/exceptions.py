from domain.entities.user.types import UserMetaIDType
from shared.errors import NotFoundError


class UserNotFoundError(NotFoundError):
    def __init__(self, user_id: UserMetaIDType) -> None:
        self.__user_id = user_id
        super().__init__(f"Пользователь не найден! -> {user_id=}")

    @property
    def user_id(self) -> UserMetaIDType:
        return self.__user_id
