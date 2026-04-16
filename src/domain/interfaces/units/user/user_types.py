from pathlib import Path

# Типы данных настроек пользователя.
type SettingsNameType = str
type SettingsAvatarPathType = Path
type SettingsTimeBlockType = int
type SettingsUpdNameType = SettingsNameType | None
type SettingsUpdAvatarPathType = SettingsAvatarPathType | None
type SettingsUpdTimeBlockType = SettingsTimeBlockType | None

# Типы данных пользователя.
type UserLoginType = str
type UserPasswordType = bytes
