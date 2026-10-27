from dishka import AsyncContainer, make_async_container

from infrastructure.config import Settings

from .providers import (
    ConnectionDBProvider,
    ConnectionStoreProvider,
    ObjectStoreProvider,
    SettingsProvider,
    UnitOfWorkProvider,
)
from .providers.card import (
    CardControllerProvider,
    CardInfoProvider,
    CardNonePresenterProvider,
    CardPresenterProvider,
    CardQueryServiceProvider,
    CardsCountProvider,
    CardUseCaseProvider,
)
from .providers.user import (
    UserControllerProvider,
    UserNonePresenterProvider,
    UserPresenterProvider,
    UserQueryServiceProvider,
    UsersCountProvider,
    UsersInfoProvider,
    UserUseCaseProvider,
)


def init_container(settings: Settings) -> AsyncContainer:
    return make_async_container(
        SettingsProvider(settings),
        ConnectionDBProvider(),
        ConnectionStoreProvider(),
        ObjectStoreProvider(),
        UnitOfWorkProvider(),

        CardControllerProvider(),
        CardNonePresenterProvider(),
        CardPresenterProvider(),
        CardsCountProvider(),
        CardInfoProvider(),
        CardQueryServiceProvider(),
        CardUseCaseProvider(),

        UserControllerProvider(),
        UserNonePresenterProvider(),
        UserPresenterProvider(),
        UsersCountProvider(),
        UsersInfoProvider(),
        UserQueryServiceProvider(),
        UserUseCaseProvider()
    )
