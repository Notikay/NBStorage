from pathlib import Path

from domain.entities import MetaData, Card


class TestMetaData:
    """Тестирование метаданных карточки пользователя."""

    METADATA_TEST_PARAMS = (
        'test_title',
        Path('./data/icon.png'),
        'test_user_login'
    )

    # === Позитивные тесты ===
    def test_create_metadata(self):
        meta = MetaData(*self.METADATA_TEST_PARAMS)
        assert meta, "Ошибка при создании метаданных карточки пользователя!"

    def test_return_metadata_key_is_not_empty(self):
        key = MetaData(*self.METADATA_TEST_PARAMS).key
        assert key, "Ключ в метаданных карточки пользователя пуст!"

    def test_return_metadata_key_is_unique(self):
        key_1 = MetaData(*self.METADATA_TEST_PARAMS).key
        key_2 = MetaData(*self.METADATA_TEST_PARAMS).key
        assert key_1 != key_2, \
            "Ключ в метаданных карточки пользователя не уникален!"

    def test_return_metadata_card_id_is_not_empty(self):
        card_id = MetaData(*self.METADATA_TEST_PARAMS).card_id
        assert card_id, "ID карточки пользователя пуст!"

    def test_return_metadata_card_id_is_unique(self):
        card_id_1 = MetaData(*self.METADATA_TEST_PARAMS).card_id
        card_id_2 = MetaData(*self.METADATA_TEST_PARAMS).card_id
        assert card_id_1 != card_id_2, "ID карточки пользователя не уникален!"

    def test_return_metadata_to_dict_is_dict_type(self):
        meta_dict = MetaData(*self.METADATA_TEST_PARAMS).to_dict()
        assert isinstance(meta_dict, dict), \
            "Ошибка преобразования метаданных карточки пользователя в словарь!"

    def test_return_metadata_to_dict_is_not_empty(self):
        meta_dict = MetaData(*self.METADATA_TEST_PARAMS).to_dict()
        assert meta_dict, "Словарь метаданных карточки пользователя пуст!"
