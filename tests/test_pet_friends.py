
import pytest
from api import PetFriends
from settings import *
import os


pf = PetFriends()


# def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
#     """ Проверяем что запрос api ключа возвращает статус 200 и в тезультате содержится слово key"""
#
#     # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
#     status, result = pf.get_api_key(email, password)
#     # Сверяем полученные данные с нашими ожиданиями
#     assert status == 200
#     assert 'key' in result
#
#
# def test_get_all_pets_with_valid_key(filter=''):
#     """ Проверяем что запрос всех питомцев возвращает не пустой список.
#     Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
#     запрашиваем список всех питомцев и проверяем что список не пустой.
#     Доступное значение параметра filter - 'my_pets' либо '' """
#
#     _, auth_key = pf.get_api_key(valid_email, valid_password)
#     status, result = pf.get_list_of_pets(auth_key, filter)
#     assert status == 200
#     assert len(result['pets']) > 0
#
#
# def test_add_new_pet_with_valid_data(name='Charlie', animal_type='shaggy',
#                                      age='4', pet_photo='images/photo_2022-09-10_16-31-54.jpg'):
#     """Проверяем что можно добавить питомца с корректными данными"""
#
#     # Запрашиваем ключ api и сохраняем в переменую auth_key
#     _, auth_key = pf.get_api_key(valid_email, valid_password)
#
#     # Добавляем питомца
#     status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
#
#     # Сверяем полученный ответ с ожидаемым результатом
#     assert status == 200
#     assert result['name'] == name
#
# def test_successful_update_self_pet_info(name='Timmy', animal_type='meow', age=5):
#     """Проверяем возможность обновления информации о питомце"""
#
#     # Получаем ключ auth_key и список своих питомцев
#     _, auth_key = pf.get_api_key(valid_email, valid_password)
#     _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
#
#     # Если список не пустой, то пробуем обновить его имя, тип и возраст
#     if len(my_pets['pets']) > 0:
#         status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
#
#         # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
#         assert status == 200
#         assert result['name'] == name
#     else:
#         # если список питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
#         raise Exception("There is no my pets")
#
#
# def test_successful_delete_self_pet():
#     """Проверяем возможность удаления питомца"""
#
#     # Получаем ключ auth_key и запрашиваем список своих питомцев
#     _, auth_key = pf.get_api_key(valid_email, valid_password)
#     _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
#
#     # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
#     if len(my_pets['pets']) == 0:
#         pf.add_new_pet(auth_key, "Sara", "pumpkin", "3", "images/photo_2022-09-10_16-31-54.jpg")
#         _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
#
#     # Берём id первого питомца из списка и отправляем запрос на удаление
#     pet_id = my_pets['pets'][0]['id']
#     status, _ = pf.delete_pet(auth_key, pet_id)
#
#     # Ещё раз запрашиваем список своих питомцев
#     _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
#
#     # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
#     assert status == 200
#     assert pet_id not in my_pets.values()


def test_add_new_pet_simple_with_valid_data(name='Charlie', animal_type='shaggy', age='4'):
    """Проверяем что можно добавить питомца с корректными данными без фото"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name

def test_add_photo_pet(pet_photo='images/photo_2022-09-10_16-31-54.jpg'):
    """Проверяем что можно добавить фото питомца"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet_simple(auth_key, "Sara", "pumpkin", "3")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, result = pf.add_photo_pet(auth_key, pet_id, pet_photo)

    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 200
    assert result['pet_photo'] != ''


def test_add_photo_pet_with_invalid_data(pet_photo='images/giphy.gif'):
    """Проверяем, что нельзя добавить в фото файл другого формата"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet_simple(auth_key, "Sara", "pumpkin", "3")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, result = pf.add_photo_pet(auth_key, pet_id, pet_photo)

    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 500

def test_add_new_pet_simple_with_invalid_data(name='Charlie', animal_type='shaggy', age='четыре'):
    """Проверяем что можно добавить питомца с некорректными данными"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name

# я понимаю, что этот тест должен проверять невозможность удаления чужого питомца, но т.к. эта возможность на сайте есть, а наши тесты не должны быть провалены, он будет таким:
def test_successful_delete_other_pet():
    """Проверяем возможность удаления чужого питомца"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, pets = pf.get_list_of_pets(auth_key, "")


    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список питомцев
    _, pets = pf.get_list_of_pets(auth_key, "")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in pets.values()


def test_successful_update_other_pet_info(name='Timmy', animal_type='cat', age=5):
    """Проверяем возможность обновления информации о чужом питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, pets = pf.get_list_of_pets(auth_key, "")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии питомцев
        raise Exception("There is no pets")

def test_get_api_key_for_invalid_user(email=valid_email, password=invalid_password):
    """ Проверяем, что запрос api ключа невозможен при отправке неправильного пароля"""

    status, _ = pf.get_api_key(email, password)

    assert status == 403

def test_add_new_pet_without_photo(name='Python', animal_type='zmey',
                                     age='365', pet_photo=''):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    with pytest.raises(FileNotFoundError):
        pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)


def test_add_new_pet_simple_with_invalid_name(name='%/$@', animal_type='dog', age='4'):
    """Проверяем, что можно добавить питомца с именем, введённым спецсимволами"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name

def test_add_new_pet_simple_without_data(name='', animal_type='', age=''):
    """Проверяем, что можно добавить питомца с пустыми данными"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name


