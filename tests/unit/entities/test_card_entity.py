from collections import namedtuple
from pathlib import Path
from uuid import UUID

import pytest

from domain.entities import CardMeta, Card
from domain.entities.card.exceptions import (
    CardMetaInvalidTitleError,
    CardMetaInvalidIconPathError,
    CardMetaInvalidUserLoginError,
    CardInvalidParamError
)

MetaTestParams = namedtuple(
    'MetaTestParams',
    ('title', 'icon_path', 'user_login')
)
CardTestParams = namedtuple(
    'CardTestParams',
    ('username', 'email', 'password', 'url', 'description')
)

META_TEST_PARAMS = MetaTestParams(
    'test_title',
    Path('./data/icon.png'),
    'test_user_login'
)
CARD_TEST_PARAMS = CardTestParams(*('test_param'.encode('utf-8'),)*5)


@pytest.fixture
def meta() -> CardMeta:
    return CardMeta(*META_TEST_PARAMS)

# === Позитивные тесты метаданных карточки пользователя ===
def test_create_meta():
    assert CardMeta(*META_TEST_PARAMS), \
        "Ошибка при создании метаданных карточки пользователя!"

def test_meta_return_correct_values():
    meta = CardMeta(*META_TEST_PARAMS)

    assert meta.title == META_TEST_PARAMS.title, \
        "Название карточки пользователя не совпадает с входным!"
    assert meta.icon_path == META_TEST_PARAMS.icon_path, \
        "Путь к иконке карточки пользователя не совпадает с входным!"
    assert meta.user_login == META_TEST_PARAMS.user_login, (
        "Логин пользователя, которому принадлежит карточка, не совпадает с "
        "входным!"
    )

def test_meta_return_key_is_not_empty():
    key = CardMeta(*META_TEST_PARAMS).key

    assert key, "Ключ в метаданных карточки пользователя пуст!"

def test_meta_return_key_is_unique():
    key = CardMeta(*META_TEST_PARAMS).key
    another_key = CardMeta(*META_TEST_PARAMS).key

    assert another_key != key, \
        "Ключ в метаданных карточки пользователя не уникален!"

def test_meta_return_card_id_is_not_empty():
    card_id = CardMeta(*META_TEST_PARAMS).card_id

    assert card_id, "ID карточки пользователя пуст!"

def test_meta_return_card_id_is_unique():
    card_id = CardMeta(*META_TEST_PARAMS).card_id
    another_card_id = CardMeta(*META_TEST_PARAMS).card_id

    assert another_card_id != card_id, "ID карточки пользователя не уникален!"

def test_meta_return_card_id_restored_from_key():
    meta = CardMeta(*META_TEST_PARAMS)
    card_id = CardMeta(
        meta.title,
        meta.icon_path,
        meta.user_login,
        meta.key
    ).card_id

    assert card_id == meta.card_id, \
        "ID карточки пользователя был восстановлен неверно!"

def test_meta_return_to_dict_is_dict_type():
    meta_dict = CardMeta(*META_TEST_PARAMS).to_dict()

    assert isinstance(meta_dict, dict), \
        "Ошибка преобразования метаданных карточки пользователя в словарь!"

def test_meta_return_to_dict_is_not_empty():
    meta_dict = CardMeta(*META_TEST_PARAMS).to_dict()

    assert meta_dict, "Словарь метаданных карточки пользователя пуст!"

def test_meta_return_to_dict_icon_path_is_str_type():
    meta_dict = CardMeta(*META_TEST_PARAMS).to_dict()

    assert isinstance(meta_dict['icon_path'], str), \
        "Путь к иконке карточки пользователя не является строкой!"

def test_meta_return_to_dict_card_id_is_str_type():
    meta_dict = CardMeta(*META_TEST_PARAMS).to_dict()

    assert isinstance(meta_dict['card_id'], str), \
        "ID карточки пользователя не является строкой!"

def test_meta_successful_to_dict_correct_values():
    meta = CardMeta(*META_TEST_PARAMS)
    meta_dict = meta.to_dict()

    assert meta_dict['title'] == meta.title, (
        "Название карточки пользователя, из словаря метаданных, не совпадает "
        "с названием из экземпляра класса!"
    )
    assert meta_dict['icon_path'] == str(meta.icon_path), (
        "Путь к иконке карточки пользователя, из словаря метаданных, не "
        "совпадает с путем из экземпляра класса!"
    )
    assert meta_dict['user_login'] == meta.user_login, (
        "Логин пользователя, которому принадлежит карточка, из словаря "
        "метаданных, не совпадает с логином из экземпляра класса!"
    )
    assert meta_dict['card_id'] == str(meta.card_id), (
        "ID карточки пользователя, из словаря метаданных, не совпадает с ID "
        "из экземпляра класса!"
    )

def test_meta_successful_generate_card_id():
    meta = CardMeta(*META_TEST_PARAMS)

    assert hasattr(meta, 'card_id'), \
        "ID карточки пользователя не был сгенерирован!"

def test_meta_successful_generate_uuid_from_login_and_key():
    meta = CardMeta(*META_TEST_PARAMS)
    uuid = meta.generate_uuid_from_login_and_key(
        META_TEST_PARAMS.user_login,
        meta.key
    )

    assert isinstance(uuid, UUID), "ID не является UUID-объектом."

# === Позитивные тесты карточки пользователя ===
def test_create_card(meta: CardMeta):
    assert Card(meta, *CARD_TEST_PARAMS), \
        "Ошибка при создании карточки пользователя!"

def test_card_return_correct_values(meta: CardMeta):
    card = Card(meta, *CARD_TEST_PARAMS)

    assert card.username == CARD_TEST_PARAMS.username, (
        "Имя пользователя от сервиса, в карточке пользователя, не совпадает с "
        "входным!"
    )
    assert card.email == CARD_TEST_PARAMS.email, (
        "Электронная почта от сервиса, в карточке пользователя, не совпадает "
        "с входным!"
    )
    assert card.password == CARD_TEST_PARAMS.password, \
        "Пароль от сервиса, в карточке пользователя, не совпадает с входным!"
    assert card.url == CARD_TEST_PARAMS.url, (
        "URL-адрес от сервиса, в карточке пользователя, не совпадает с "
        "входным!"
    )
    assert card.description == CARD_TEST_PARAMS.description, \
        "Описание сервиса, в карточке пользователя, не совпадает с входным!"

def test_card_return_to_dict_is_dict_type(meta: CardMeta):
    card_dict = Card(meta, *CARD_TEST_PARAMS).to_dict()

    assert isinstance(card_dict, dict), \
        "Ошибка преобразования карточки пользователя в словарь!"

def test_card_return_to_dict_is_not_empty(meta: CardMeta):
    card_dict = Card(meta, *CARD_TEST_PARAMS).to_dict()

    assert card_dict, "Словарь карточки пользователя пуст!"

def test_card_successful_to_dict_correct_meta(meta: CardMeta):
    card = Card(meta, *CARD_TEST_PARAMS)
    card_dict = card.to_dict()

    assert card_dict['meta'] == card.meta.to_dict(), (
        "Метаданные карточки пользователя, из словаря карточки пользователя, "
        "не совпадают с метаданными из экземпляра класса!"
    )

def test_card_successful_to_dict_correct_values(meta: CardMeta):
    card = Card(meta, *CARD_TEST_PARAMS)
    card_dict = card.to_dict()

    assert card.username is not None, \
        "Имя пользователя от сервиса, в карточке пользователя, является None!"
    assert card.email is not None, \
        "Электронная почта от сервиса, в карточке пользователя, является None!"
    assert card.password is not None, \
        "Пароль от сервиса, в карточке пользователя, является None!"
    assert card.url is not None, \
        "URL-адрес от сервиса, в карточке пользователя, является None!"
    assert card.description is not None, \
        "Описание сервиса, в карточке пользователя, является None!"

    assert card_dict['username'] == card.username.decode('utf-8'), (
        "Имя пользователя от сервиса, из словаря карточки пользователя, не "
        "совпадает с именем пользователя от сервиса из экземпляра класса!"
    )
    assert card_dict['email'] == card.email.decode('utf-8'), (
        "Электронная почта от сервиса, из словаря карточки пользователя, не "
        "совпадает с электронной почтой от сервиса из экземпляра класса!"
    )
    assert card_dict['password'] == card.password.decode('utf-8'), (
        "Пароль от сервиса, из словаря карточки пользователя, не совпадает с "
        "паролем от сервиса из экземпляра класса!"
    )
    assert card_dict['url'] == card.url.decode('utf-8'), (
        "URL-адрес от сервиса, из словаря карточки пользователя, не совпадает "
        "с URL-адресом от сервиса из экземпляра класса!"
    )
    assert card_dict['description'] == card.description.decode('utf-8'), (
        "Описание сервиса, из словаря карточки пользователя, не совпадает с "
        "описанием сервиса из экземпляра класса!"
    )

def test_card_successful_to_dict_correct_none(meta: CardMeta):
    card_dict = Card(meta, None, None, None, None, None).to_dict()

    assert card_dict['username'] is None, (
        "Имя пользователя от сервиса, из словаря карточки пользователя, не "
        "является None!"
    )
    assert card_dict['email'] is None, (
        "Электронная почта от сервиса, из словаря карточки пользователя, не "
        "является None!"
    )
    assert card_dict['password'] is None, (
        "Пароль от сервиса, из словаря карточки пользователя, не является "
        "None!"
    )
    assert card_dict['url'] is None, (
        "URL-адрес от сервиса, из словаря карточки пользователя, не является "
        "None!"
    )
    assert card_dict['description'] is None, \
        "Описание сервиса, из словаря карточки пользователя, не является None!"

def test_card_return_encrypt_change_params(meta: CardMeta):
    card = Card(meta, *CARD_TEST_PARAMS)
    card.encrypt()

    assert card.username != CARD_TEST_PARAMS.username, (
        "Имя пользователя от сервиса, в карточке пользователя, не было "
        "зашифровано!"
    )
    assert card.email != CARD_TEST_PARAMS.email, (
        "Электронная почта от сервиса, в карточке пользователя, не была "
        "зашифрована!"
    )
    assert card.password != CARD_TEST_PARAMS.password, \
        "Пароль от сервиса, в карточке пользователя, не был зашифрован!"
    assert card.url != CARD_TEST_PARAMS.url, \
        "URL-адрес от сервиса, в карточке пользователя, не был зашифрован!"
    assert card.description != CARD_TEST_PARAMS.description, \
        "Описание сервиса, в карточке пользователя, не было зашифровано!"

def test_card_return_encrypt_not_change_none_params(meta: CardMeta):
    card_none = Card(meta, None, None, None, None, None)
    card_none.encrypt()

    assert card_none.username is None, (
        "Имя пользователя от сервиса, в карточке пользователя, не является "
        "None!"
    )
    assert card_none.email is None, (
        "Электронная почта от сервиса, в карточке пользователя, не является "
        "None!"
    )
    assert card_none.password is None, \
        "Пароль от сервиса, в карточке пользователя, не является None!"
    assert card_none.url is None, \
        "URL-адрес от сервиса, в карточке пользователя, не является None!"
    assert card_none.description is None, \
        "Описание сервиса, в карточке пользователя, не является None!"

def test_card_return_decrypt_change_params(meta: CardMeta):
    card = Card(meta, *CARD_TEST_PARAMS)
    card.decrypt()

    assert card.username != CARD_TEST_PARAMS.username, (
        "Имя пользователя от сервиса, в карточке пользователя, не было "
        "расшифровано!"
    )
    assert card.email != CARD_TEST_PARAMS.email, (
        "Электронная почта от сервиса, в карточке пользователя, не была "
        "расшифрована!"
    )
    assert card.password != CARD_TEST_PARAMS.password, \
        "Пароль от сервиса, в карточке пользователя, не был расшифрован!"
    assert card.url != CARD_TEST_PARAMS.url, \
        "URL-адрес от сервиса, в карточке пользователя, не был расшифрован!"
    assert card.description != CARD_TEST_PARAMS.description, \
        "Описание сервиса, в карточке пользователя, не было расшифровано!"

def test_card_return_decrypt_not_change_none_params(meta: CardMeta):
    card_none = Card(meta, None, None, None, None, None)
    card_none.decrypt()

    assert card_none.username is None, (
        "Имя пользователя от сервиса, в карточке пользователя, не является "
        "None!"
    )
    assert card_none.email is None, (
        "Электронная почта от сервиса, в карточке пользователя, не является "
        "None!"
    )
    assert card_none.password is None, \
        "Пароль от сервиса, в карточке пользователя, не является None!"
    assert card_none.url is None, \
        "URL-адрес от сервиса, в карточке пользователя, не является None!"
    assert card_none.description is None, \
        "Описание сервиса, в карточке пользователя, не является None!"

def test_card_successful_encrypt_decrypt_pipeline(meta: CardMeta):
    card = Card(meta, *CARD_TEST_PARAMS)
    card.encrypt()
    card.decrypt()

    assert card.username == CARD_TEST_PARAMS.username, (
        "Результат шифровки и расшифровки имени пользователя от сервиса "
        "прошел некорректно!"
    )
    assert card.email == CARD_TEST_PARAMS.email, (
        "Результат шифровки и расшифровки электронной почты от сервиса прошел "
        "некорректно!"
    )
    assert card.password == CARD_TEST_PARAMS.password, (
        "Результат шифровки и расшифровки пароля от сервиса прошел "
        "некорректно!"
    )
    assert card.url == CARD_TEST_PARAMS.url, (
        "Результат шифровки и расшифровки URL-адреса от сервиса прошел "
        "некорректно!"
    )
    assert card.description == CARD_TEST_PARAMS.description, \
        "Результат шифровки и расшифровки описания сервиса прошел некорректно!"

def test_card_successful_encrypt_decrypt_pipeline_for_several_cards(
        meta: CardMeta
):
    card = Card(meta, *CARD_TEST_PARAMS)
    card.encrypt()

    another_meta = CardMeta(*META_TEST_PARAMS)
    another_card = Card(another_meta, *CARD_TEST_PARAMS)
    another_card.encrypt()

    assert another_card.username != card.username, (
        "Результат шифровки имени пользователя от сервиса, для разных "
        "карточек пользователей, одинаков!"
    )
    assert another_card.email != card.email, (
        "Результат шифровки электронной почты от сервиса, для разных карточек "
        "пользователей, одинаков!"
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

def test_card_successful_check_is_encrypted_flag(meta: CardMeta):
    card = Card(meta, *CARD_TEST_PARAMS)
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

def test_card_return_xor_otp_encrypt_is_none(meta: CardMeta):
    card = Card(meta, *CARD_TEST_PARAMS)
    encrypted_param = card.xor_otp_encrypt(None, card.meta.key)

    assert encrypted_param is None, \
        "Результат шифровки None, не является None!"

def test_card_successful_xor_otp_encrypt(meta: CardMeta):
    card = Card(meta, *CARD_TEST_PARAMS)
    encrypted_param = card.xor_otp_encrypt(
        CARD_TEST_PARAMS.username,
        card.meta.key
    )

    assert encrypted_param != CARD_TEST_PARAMS.username, \
        "Результат шифровки параметра не отличается от исходного!"

    decrypt_param = card.xor_otp_encrypt(encrypted_param, card.meta.key)

    assert decrypt_param == CARD_TEST_PARAMS.username, \
        "Результат расшифровки параметра не совпадает с исходным!"

# === Негативные тесты метаданных карточки пользователя ===
def test_meta_raises_invalid_title_is_empty():
    with pytest.raises(CardMetaInvalidTitleError):
        CardMeta('', META_TEST_PARAMS.icon_path, META_TEST_PARAMS.user_login)

def test_meta_raises_invalid_icon_path_incorrect_ext():
    with pytest.raises(CardMetaInvalidIconPathError):
        CardMeta(
            META_TEST_PARAMS.title,
            Path('./icon.bad_ext'),
            META_TEST_PARAMS.user_login
        )

def test_meta_raises_invalid_icon_path_is_empty():
    with pytest.raises(CardMetaInvalidIconPathError):
        CardMeta(META_TEST_PARAMS.title, Path(''), META_TEST_PARAMS.user_login)

def test_meta_raises_invalid_user_login_is_empty():
    with pytest.raises(CardMetaInvalidUserLoginError):
        CardMeta(META_TEST_PARAMS.title, META_TEST_PARAMS.icon_path, '')

# === Негативные тесты карточки пользователя ===
def test_card_raises_card_invalid_param_field_is_equal_key(meta: CardMeta):
    with pytest.raises(CardInvalidParamError):
        Card(meta, meta.key, None, None, None, None)

def test_card_raises_invalid_param_field_is_empty(meta: CardMeta):
    with pytest.raises(CardInvalidParamError):
        Card(meta, b'', None, None, None, None)

def test_card_raises_invalid_param_field_with_key_start(meta: CardMeta):
    test_param = meta.key[:5]
    with pytest.raises(CardInvalidParamError):
        Card(meta, test_param, None, None, None, None)
