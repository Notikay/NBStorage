from uuid import UUID

# Типы метаданных пользователя.
type UserMetaNameType = str
type UserMetaAvatarIsThereType = str
type UserMetaAvatarKeyType = UserMetaAvatarIsThereType | None
type UserMetaTimeBlockType = int
type UserMetaIDType = UUID
type UserMetaSaltType = bytes
type UserMetaUpdNameType = UserMetaNameType | None
type UserMetaUpdTimeBlockType = UserMetaTimeBlockType | None

# Типы данных пользователя.
type UserLoginType = str
type UserPasswordType = bytes
type UserUpdLoginType = UserLoginType | None
type UserUpdPasswordType = UserPasswordType | None
