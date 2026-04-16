from abc import ABCMeta, abstractmethod

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm.decl_api import DeclarativeAttributeIntercept


class BaseMeta(DeclarativeAttributeIntercept, ABCMeta):
    pass


class Base(DeclarativeBase, metaclass=BaseMeta):

    @abstractmethod
    def to_item(self):
        pass
