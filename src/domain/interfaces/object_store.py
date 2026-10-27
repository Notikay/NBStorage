from typing import Protocol

type KeyType = str


class ObjectStore(Protocol):
    def save(self, key: KeyType, content: bytes, content_type: str) -> None: ...

    def delete(self, key: KeyType) -> None: ...

    def get_url(self, key: KeyType, private: bool = False) -> str: ...
