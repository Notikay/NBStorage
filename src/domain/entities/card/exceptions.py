from shared.errors import MessageType, ValidationError

from .types import CardMetaIconKeyType, CardMetaTitleType, CardParamType

type ParamNameType = str


class CardMetaInvalidTitleError(ValidationError):
    def __init__(self, title: CardMetaTitleType) -> None:
        self.__title = title
        super().__init__(f"Некорректное название карточки пользователя! -> {title=}")

    @property
    def title(self) -> CardMetaTitleType:
        return self.__title


class CardMetaInvalidIconKeyError(ValidationError):
    def __init__(self, icon_key: CardMetaIconKeyType) -> None:
        self.__icon_key = icon_key
        super().__init__(
            f"Некорректный ключ иконки карточки пользователя! -> {icon_key=}"
        )

    @property
    def icon_key(self) -> CardMetaIconKeyType:
        return self.__icon_key


class CardInvalidParamError(ValidationError):
    def __init__(
            self,
            param: CardParamType,
            param_name: ParamNameType,
            msg: MessageType | None = None
    ) -> None:
        self.__param = param
        self.__param_name = param_name

        if msg:
            message = f"{msg} -> {param_name=}: {param=!r}"
        else:
            message = ("Некорректное значение параметра в карточке пользователя! -> "
                       f"{param_name=}: {param=!r}")
        super().__init__(message)

    @property
    def param_name_with_param(self) -> dict[ParamNameType, CardParamType]:
        return {self.__param_name: self.__param}
