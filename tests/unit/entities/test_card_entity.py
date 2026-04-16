from pathlib import Path

import pytest

from domain.entities import MetaData, Card
from domain.entities.card.exceptions import (
    MetaDataInvalidTitleError,
    MetaDataInvalidIconPathError,
    MetaDataInvalidUserLoginError,
    CardInvalidParamFieldError
)


class TestMetaData:
    """Тестирование метаданных карточки пользователя."""

    METADATA_TEST_PARAMS = (
        'test_title',
        Path('./data/icon.png'),
        'test_user_login'
    )

    # === Позитивные тесты ===
    def test_create_metadata(self):
        assert MetaData(*self.METADATA_TEST_PARAMS), \
            "Ошибка при создании метаданных карточки пользователя!"

    def test_metadata_return_correct_values(self):
        metadata = MetaData(*self.METADATA_TEST_PARAMS)

        assert metadata.title == self.METADATA_TEST_PARAMS[0], \
            "Название карточки пользователя не совпадает с входным!"
        assert metadata.icon_path == self.METADATA_TEST_PARAMS[1], \
            "Путь к иконке карточки пользователя не совпадает с входным!"
        assert metadata.user_login == self.METADATA_TEST_PARAMS[2], (
            "Логин пользователя, которому принадлежит карточка, не совпадает "
            "с входным!"
        )

    def test_metadata_return_key_is_not_empty(self):
        key = MetaData(*self.METADATA_TEST_PARAMS).key

        assert key, "Ключ в метаданных карточки пользователя пуст!"

    def test_metadata_return_key_is_unique(self):
        key = MetaData(*self.METADATA_TEST_PARAMS).key
        another_key = MetaData(*self.METADATA_TEST_PARAMS).key

        assert another_key != key, \
            "Ключ в метаданных карточки пользователя не уникален!"

    def test_metadata_return_card_id_is_not_empty(self):
        card_id = MetaData(*self.METADATA_TEST_PARAMS).card_id

        assert card_id, "ID карточки пользователя пуст!"

    def test_metadata_return_card_id_is_unique(self):
        card_id = MetaData(*self.METADATA_TEST_PARAMS).card_id
        another_card_id = MetaData(*self.METADATA_TEST_PARAMS).card_id

        assert another_card_id != card_id, \
            "ID карточки пользователя не уникален!"

    def test_metadata_return_card_id_restored_from_key(self):
        metadata = MetaData(*self.METADATA_TEST_PARAMS)
        card_id = MetaData(
            metadata.title,
            metadata.icon_path,
            metadata.user_login,
            metadata.key
        ).card_id

        assert card_id == metadata.card_id, \
            "ID карточки пользователя был восстановлен неверно!"

    def test_metadata_return_to_dict_is_dict_type(self):
        metadata_dict = MetaData(*self.METADATA_TEST_PARAMS).to_dict()

        assert isinstance(metadata_dict, dict), \
            "Ошибка преобразования метаданных карточки пользователя в словарь!"

    def test_metadata_return_to_dict_is_not_empty(self):
        metadata_dict = MetaData(*self.METADATA_TEST_PARAMS).to_dict()

        assert metadata_dict, "Словарь метаданных карточки пользователя пуст!"

    def test_metadata_return_to_dict_icon_path_is_str_type(self):
        metadata_dict = MetaData(*self.METADATA_TEST_PARAMS).to_dict()

        assert isinstance(metadata_dict['icon_path'], str), \
            "Путь к иконке карточки пользователя не является строкой!"

    def test_metadata_return_to_dict_card_id_is_str_type(self):
        metadata_dict = MetaData(*self.METADATA_TEST_PARAMS).to_dict()

        assert isinstance(metadata_dict['card_id'], str), \
            "ID карточки пользователя не является строкой!"

    def test_metadata_successful_to_dict_correct_values(self):
        metadata = MetaData(*self.METADATA_TEST_PARAMS)
        metadata_dict = metadata.to_dict()

        assert metadata_dict['title'] == metadata.title, (
            "Название карточки пользователя, из словаря метаданных, не "
            "совпадает с названием из экземпляра класса!"
        )
        assert metadata_dict['icon_path'] == str(metadata.icon_path), (
            "Путь к иконке карточки пользователя, из словаря метаданных, не "
            "совпадает с путем из экземпляра класса!"
        )
        assert metadata_dict['user_login'] == metadata.user_login, (
            "Логин пользователя, которому принадлежит карточка, из словаря "
            "метаданных, не совпадает с логином из экземпляра класса!"
        )
        assert metadata_dict['card_id'] == str(metadata.card_id), (
            "ID карточки пользователя, из словаря метаданных, не совпадает с "
            "ID из экземпляра класса!"
        )

    # === Негативные тесты ===
    def test_metadata_raises_invalid_title_is_empty(self):
        with pytest.raises(MetaDataInvalidTitleError):
            MetaData('', Path('./icon.png'), 'test_user_login')

    def test_metadata_raises_invalid_icon_path_incorrect_ext(self):
        with pytest.raises(MetaDataInvalidIconPathError):
            MetaData('test_title', Path('./icon.bad_ext'), 'test_user_login')

    def test_metadata_raises_invalid_icon_path_is_empty(self):
        with pytest.raises(MetaDataInvalidIconPathError):
            MetaData('test_title', Path(''), 'test_user_login')

    def test_metadata_raises_invalid_user_login_is_empty(self):
        with pytest.raises(MetaDataInvalidUserLoginError):
            MetaData('test_title', Path('./icon.png'), '')


class TestCard:
    """Тестирование карточки пользователя."""

    METADATA_TEST_PARAMS = (
        'test_title',
        Path('./data/icon.png'),
        'test_user_login'
    )
    CARD_TEST_PARAMS = ('test_param'.encode('utf-8'),)*5

    @pytest.fixture
    def metadata(self) -> MetaData:
        return MetaData(*self.METADATA_TEST_PARAMS)

    # === Позитивные тесты ===
    def test_create_card(self, metadata: MetaData):
        assert Card(metadata, *self.CARD_TEST_PARAMS), \
            "Ошибка при создании карточки пользователя!"

    def test_card_return_correct_values(self, metadata: MetaData):
        card = Card(metadata, *self.CARD_TEST_PARAMS)

        assert card.username == self.CARD_TEST_PARAMS[0], (
            "Имя пользователя от сервиса, в карточке пользователя, не "
            "совпадает с входным!"
        )
        assert card.email == self.CARD_TEST_PARAMS[1], (
            "Электронная почта от сервиса, в карточке пользователя, не "
            "совпадает с входным!"
        )
        assert card.password == self.CARD_TEST_PARAMS[2], (
            "Пароль от сервиса, в карточке пользователя, не совпадает с "
            "входным!"
        )
        assert card.url == self.CARD_TEST_PARAMS[3], (
            "URL-адрес от сервиса, в карточке пользователя, не совпадает с "
            "входным!"
        )
        assert card.description == self.CARD_TEST_PARAMS[4], (
            "Описание сервиса, в карточке пользователя, не совпадает с "
            "входным!"
        )

    def test_card_return_to_dict_is_dict_type(self, metadata: MetaData):
        card_dict = Card(metadata, *self.CARD_TEST_PARAMS).to_dict()

        assert isinstance(card_dict, dict), \
            "Ошибка преобразования карточки пользователя в словарь!"

    def test_card_return_to_dict_is_not_empty(self, metadata: MetaData):
        card_dict = Card(metadata, *self.CARD_TEST_PARAMS).to_dict()

        assert card_dict, "Словарь карточки пользователя пуст!"

    def test_card_successful_to_dict_correct_metadata(self, metadata: MetaData):
        card = Card(metadata, *self.CARD_TEST_PARAMS)
        card_dict = card.to_dict()

        assert card_dict['metadata'] == card.metadata.to_dict(), (
            "Метаданные карточки пользователя, из словаря карточки "
            "пользователя, не совпадают с метаданными из экземпляра класса!"
        )

    def test_card_successful_to_dict_correct_values(self, metadata: MetaData):
        card = Card(metadata, *self.CARD_TEST_PARAMS)
        card_dict = card.to_dict()

        assert card.username is not None, (
            "Имя пользователя от сервиса, в карточке пользователя, является "
            "None!"
        )
        assert card.email is not None, (
            "Электронная почта от сервиса, в карточке пользователя, является "
            "None!"
        )
        assert card.password is not None, \
            "Пароль от сервиса, в карточке пользователя, является None!"
        assert card.url is not None, \
            "URL-адрес от сервиса, в карточке пользователя, является None!"
        assert card.description is not None, \
            "Описание сервиса, в карточке пользователя, является None!"

        assert card_dict['username'] == card.username.decode('utf-8'), (
            "Имя пользователя от сервиса, из словаря карточки пользователя, "
            "не совпадает с именем пользователя от сервиса из экземпляра "
            "класса!"
        )
        assert card_dict['email'] == card.email.decode('utf-8'), (
            "Электронная почта от сервиса, из словаря карточки пользователя, "
            "не совпадает с электронной почтой от сервиса из экземпляра "
            "класса!"
        )
        assert card_dict['password'] == card.password.decode('utf-8'), (
            "Пароль от сервиса, из словаря карточки пользователя, не "
            "совпадает с паролем от сервиса из экземпляра класса!"
        )
        assert card_dict['url'] == card.url.decode('utf-8'), (
            "URL-адрес от сервиса, из словаря карточки пользователя, не "
            "совпадает с URL-адресом от сервиса из экземпляра класса!"
        )
        assert card_dict['description'] == card.description.decode('utf-8'), (
            "Описание сервиса, из словаря карточки пользователя, не совпадает "
            "с описанием сервиса из экземпляра класса!"
        )

    def test_card_successful_to_dict_correct_none(self, metadata: MetaData):
        card_dict = Card(metadata, None, None, None, None, None).to_dict()

        assert card_dict['username'] is None, (
            "Имя пользователя от сервиса, из словаря карточки пользователя, "
            "не является None!"
        )
        assert card_dict['email'] is None, (
            "Электронная почта от сервиса, из словаря карточки пользователя, "
            "не является None!"
        )
        assert card_dict['password'] is None, (
            "Пароль от сервиса, из словаря карточки пользователя, не является "
            "None!"
        )
        assert card_dict['url'] is None, (
            "URL-адрес от сервиса, из словаря карточки пользователя, не "
            "является None!"
        )
        assert card_dict['description'] is None, (
            "Описание сервиса, из словаря карточки пользователя, не является "
            "None!"
        )

    def test_card_return_encrypt_change_params(self, metadata: MetaData):
        card = Card(metadata, *self.CARD_TEST_PARAMS)
        card.encrypt()

        assert card.username != self.CARD_TEST_PARAMS[0], (
            "Имя пользователя от сервиса, в карточке пользователя, не было "
            "зашифровано!"
        )
        assert card.email != self.CARD_TEST_PARAMS[1], (
            "Электронная почта от сервиса, в карточке пользователя, не была "
            "зашифрована!"
        )
        assert card.password != self.CARD_TEST_PARAMS[2], \
            "Пароль от сервиса, в карточке пользователя, не был зашифрован!"
        assert card.url != self.CARD_TEST_PARAMS[3], \
            "URL-адрес от сервиса, в карточке пользователя, не был зашифрован!"
        assert card.description != self.CARD_TEST_PARAMS[4], \
            "Описание сервиса, в карточке пользователя, не было зашифровано!"

    def test_card_return_encrypt_not_change_none_params(
            self,
            metadata: MetaData
    ):
        card_none = Card(metadata, None, None, None, None, None)
        card_none.encrypt()

        assert card_none.username is None, (
            "Имя пользователя от сервиса, в карточке пользователя, не "
            "является None!"
        )
        assert card_none.email is None, (
            "Электронная почта от сервиса, в карточке пользователя, не "
            "является None!"
        )
        assert card_none.password is None, \
            "Пароль от сервиса, в карточке пользователя, не является None!"
        assert card_none.url is None, \
            "URL-адрес от сервиса, в карточке пользователя, не является None!"
        assert card_none.description is None, \
            "Описание сервиса, в карточке пользователя, не является None!"

    def test_card_return_decrypt_change_params(self, metadata: MetaData):
        card = Card(metadata, *self.CARD_TEST_PARAMS)
        card.decrypt()

        assert card.username != self.CARD_TEST_PARAMS[0], (
            "Имя пользователя от сервиса, в карточке пользователя, не было "
            "расшифровано!"
        )
        assert card.email != self.CARD_TEST_PARAMS[1], (
            "Электронная почта от сервиса, в карточке пользователя, не была "
            "расшифрована!"
        )
        assert card.password != self.CARD_TEST_PARAMS[2], \
            "Пароль от сервиса, в карточке пользователя, не был расшифрован!"
        assert card.url != self.CARD_TEST_PARAMS[3], (
            "URL-адрес от сервиса, в карточке пользователя, не был "
            "расшифрован!"
        )
        assert card.description != self.CARD_TEST_PARAMS[4], \
            "Описание сервиса, в карточке пользователя, не было расшифровано!"

    def test_card_return_decrypt_not_change_none_params(
            self,
            metadata: MetaData
    ):
        card_none = Card(metadata, None, None, None, None, None)
        card_none.decrypt()

        assert card_none.username is None, (
            "Имя пользователя от сервиса, в карточке пользователя, не "
            "является None!"
        )
        assert card_none.email is None, (
            "Электронная почта от сервиса, в карточке пользователя, не "
            "является None!"
        )
        assert card_none.password is None, \
            "Пароль от сервиса, в карточке пользователя, не является None!"
        assert card_none.url is None, \
            "URL-адрес от сервиса, в карточке пользователя, не является None!"
        assert card_none.description is None, \
            "Описание сервиса, в карточке пользователя, не является None!"

    def test_card_successful_encrypt_decrypt_pipeline(
            self,
            metadata: MetaData
    ):
        card = Card(metadata, *self.CARD_TEST_PARAMS)
        card.encrypt()
        card.decrypt()

        assert card.username == self.CARD_TEST_PARAMS[0], (
            "Результат шифровки и расшифровки имени пользователя от сервиса "
            "прошел некорректно!"
        )
        assert card.email == self.CARD_TEST_PARAMS[1], (
            "Результат шифровки и расшифровки электронной почты от сервиса "
            "прошел некорректно!"
        )
        assert card.password == self.CARD_TEST_PARAMS[2], (
            "Результат шифровки и расшифровки пароля от сервиса прошел "
            "некорректно!"
        )
        assert card.url == self.CARD_TEST_PARAMS[3], (
            "Результат шифровки и расшифровки URL-адреса от сервиса прошел "
            "некорректно!"
        )
        assert card.description == self.CARD_TEST_PARAMS[4], (
            "Результат шифровки и расшифровки описания сервиса прошел "
            "некорректно!"
        )

    def test_card_successful_encrypt_decrypt_pipeline_for_several_cards(
            self,
            metadata: MetaData
    ):
        card = Card(metadata, *self.CARD_TEST_PARAMS)
        card.encrypt()

        another_metadata = MetaData(*self.METADATA_TEST_PARAMS)
        another_card = Card(another_metadata, *self.CARD_TEST_PARAMS)
        another_card.encrypt()

        assert another_card.username != card.username, (
            "Результат шифровки имени пользователя от сервиса, для разных "
            "карточек пользователей, одинаков!"
        )
        assert another_card.email != card.email, (
            "Результат шифровки электронной почты от сервиса, для разных "
            "карточек пользователей, одинаков!"
        )
        assert another_card.password != card.password, (
            "Результат шифровки пароля от сервиса, для разных карточек "
            "пользователей, одинаков!"
        )
        assert another_card.url != card.url, (
            "Результат шифровки URL-адреса от сервиса, для разных карточек "
            "пользователей, одинаков!"
        )
        assert another_card.description != card.description, (
            "Результат шифровки описания сервиса, для разных карточек "
            "пользователей, одинаков!"
        )

        card.decrypt()
        another_card.decrypt()

        assert another_card.username == card.username, (
            "Результат расшифровки имени пользователя от сервиса, для разных "
            "карточек пользователей с одинаковыми данными, разный!"
        )
        assert another_card.email == card.email, (
            "Результат расшифровки электронной почты от сервиса, для разных "
            "карточек пользователей с одинаковыми данными, разный!"
        )
        assert another_card.password == card.password, (
            "Результат расшифровки пароля от сервиса, для разных карточек "
            "пользователей с одинаковыми данными, разный!"
        )
        assert another_card.url == card.url, (
            "Результат расшифровки URL-адреса от сервиса, для разных карточек "
            "пользователей с одинаковыми данными, разный!"
        )
        assert another_card.description == card.description, (
            "Результат расшифровки описания сервиса, для разных карточек "
            "пользователей с одинаковыми данными, разный!"
        )

    def test_card_successful_check_is_encrypted_flag(self, metadata: MetaData):
        card = Card(metadata, *self.CARD_TEST_PARAMS)
        card.encrypt()

        assert card.is_encrypted, (
            "Флаг шифровки показывает, что данные карточки пользователя не "
            "зашифрованы!"
        )

        card.decrypt()

        assert not card.is_encrypted, (
            "Флаг шифровки показывает, что данные карточки пользователя "
            "зашифрованы!"
        )

    def test_card_return_xor_otp_encrypt_is_none(self, metadata: MetaData):
        card = Card(metadata, *self.CARD_TEST_PARAMS)
        encrypted_param = card.xor_otp_encrypt(None, card.metadata.key)

        assert encrypted_param is None, \
            "Результат шифровки None, не является None!"

    def test_card_successful_xor_otp_encrypt(self, metadata: MetaData):
        card = Card(metadata, *self.CARD_TEST_PARAMS)
        encrypted_param = card.xor_otp_encrypt(
            self.CARD_TEST_PARAMS[0],
            card.metadata.key
        )

        assert encrypted_param != self.CARD_TEST_PARAMS[0], \
            "Результат шифровки параметра не отличается от исходного!"

        decrypt_param = card.xor_otp_encrypt(
            encrypted_param,
            card.metadata.key
        )

        assert decrypt_param == self.CARD_TEST_PARAMS[0], \
            "Результат расшифровки параметра не совпадает с исходным!"

    # === Негативные тесты ===
    def test_card_raises_card_invalid_param_field_is_equal_key(
            self,
            metadata: MetaData
    ):
        with pytest.raises(CardInvalidParamFieldError):
            Card(metadata, metadata.key, None, None, None, None)

    def test_card_raises_invalid_param_field_is_empty(
            self,
            metadata: MetaData
    ):
        with pytest.raises(CardInvalidParamFieldError):
            Card(metadata, b'', None, None, None, None)

    def test_card_raises_invalid_param_field_with_key_start(
            self,
            metadata: MetaData
    ):
        test_param = metadata.key[:5]
        with pytest.raises(CardInvalidParamFieldError):
            Card(metadata, test_param, None, None, None, None)
