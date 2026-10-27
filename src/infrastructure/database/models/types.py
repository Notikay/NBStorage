from uuid import UUID

# Для ORM-модели карточки пользователя.
type CardModelCardIDType = UUID
type CardModelUserIDType = UUID
type CardModelTitleType = str
type CardModelIconKeyType = str | None
type CardModelKeyType = bytes
type CardModelParamType = bytes | None

# Для ORM-модели пользователя.
type UserModelIDType = UUID
type UserModelNameType = str
type UserModelAvatarKeyType = str | None
type UserModelTimeBlockType = int
type UserModelSaltType = bytes
type UserModelLoginType = str
type UserModelPasswordType = bytes
