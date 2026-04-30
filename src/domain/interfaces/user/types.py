from pathlib import Path

# Типы метаданных пользователя.
type UserMetaNameType = str
type UserMetaAvatarPathType = Path
type UserMetaTimeBlockType = int
type UserMetaSaltType = bytes
type UserMetaUpdNameType = UserMetaNameType | None
type UserMetaUpdAvatarPathType = UserMetaAvatarPathType | None
type UserMetaUpdTimeBlockType = UserMetaTimeBlockType | None

# Типы данных пользователя.
type UserLoginType = str
type UserPasswordType = bytes

type UserMessageType = str  # Тип сообщения об ошибке.
