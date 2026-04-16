from pathlib import Path
from uuid import UUID

# Типы метаданных карточки пользователя.
type MetaDataTitleType = str
type MetaDataIconPathType = Path
type MetaDataUserLoginType = str
type MetaDataCardIDType = UUID
type MetaDataUpdTitleType = MetaDataTitleType | None
type MetaDataUpdIconPathType = MetaDataIconPathType | None

# Типы данных карточки пользователя.
type CardParamType = bytes | None
type CardUpdParamType = CardParamType | None
