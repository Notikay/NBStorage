from uuid import UUID

from pydantic import SecretStr

type UserSchemaIDType = UUID
type UserSchemaNameType = str
type UserSchemaAvatarKeyType = str
type UserSchemaTimeBlockType = int
type UserSchemaLoginType = str
type UserSchemaPasswordType = SecretStr
