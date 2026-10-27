from uuid import UUID

from pydantic import EmailStr, HttpUrl, SecretStr

type CardSchemaIDType = UUID
type CardSchemaUserIDType = UUID
type CardSchemaTitleType = str
type CardSchemaUsernameType = str | None
type CardSchemaEmailType = EmailStr | None
type CardSchemaPasswordType = SecretStr | None
type CardSchemaUrlType = HttpUrl | None
type CardSchemaDescriptionType = str | None
