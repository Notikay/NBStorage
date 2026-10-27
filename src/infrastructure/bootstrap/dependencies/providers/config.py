from dishka import Provider, Scope, provide

from infrastructure.config.settings import DBSettings, Settings, StoreSettings


class SettingsProvider(Provider):
    scope = Scope.APP

    def __init__(self, settings: Settings) -> None:
        super().__init__()
        self.__settings = settings

    @provide
    def provide_database(self) -> DBSettings:
        return self.__settings.database

    @provide
    def provide_store(self) -> StoreSettings:
        return self.__settings.store
