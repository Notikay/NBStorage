from pathlib import Path
from uuid import UUID

# Типы метаданных карточки пользователя.
type CardMetaTitleType = str
type CardMetaIconPathType = Path
type CardMetaUserLoginType = str
type CardMetaKeyType = bytes
type CardMetaCardIDType = UUID
type CardMetaUpdTitleType = CardMetaTitleType | None
type CardMetaUpdIconPathType = CardMetaIconPathType | None

# Типы данных карточки пользователя.
type CardParamIsThereType = bytes
type CardParamType = CardParamIsThereType | None
type CardUpdParamType = CardParamType | None

type CardMessageType = str  # Тип сообщения об ошибке.
