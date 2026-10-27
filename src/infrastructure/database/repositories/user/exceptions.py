from domain.entities.user.types import UserMetaIDType
from shared.errors import MessageType, StorageError


class UserStorageError(StorageError):
    def __init__(self, message: MessageType, user_id: UserMetaIDType) -> None:
        super().__init__(message)
        self.__user_id = user_id

    @property
    def user_id(self) -> UserMetaIDType:
        return self.__user_id


class GetUserError(UserStorageError):
    def __init__(self, user_id: UserMetaIDType) -> None:
        super().__init__(f"Не удалось получить пользователя! -> {user_id=}", user_id)


class SaveUserError(UserStorageError):
    def __init__(self, user_id: UserMetaIDType) -> None:
        super().__init__(f"Не удалось сохранить пользователя! -> {user_id=}", user_id)


class DeleteUserError(UserStorageError):
    def __init__(self, user_id: UserMetaIDType) -> None:
        super().__init__(f"Не удалось удалить пользователя! -> {user_id=}", user_id)


class DeleteAllUsersError(StorageError):
    def __init__(self) -> None:
        super().__init__("Не удалось удалить всех пользователей!")
