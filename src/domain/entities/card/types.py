from uuid import UUID

# Типы метаданных карточки пользователя.
type CardMetaTitleType = str
type CardMetaIconIsThereType = str
type CardMetaIconKeyType = CardMetaIconIsThereType | None
type CardMetaUserIDType = UUID
type CardMetaKeyType = bytes
type CardMetaIDType = UUID
type CardMetaUpdTitleType = CardMetaTitleType | None

# Типы данных карточки пользователя.
type CardParamIsThereType = bytes
type CardParamType = CardParamIsThereType | None
type CardUpdParamType = CardParamType | None
