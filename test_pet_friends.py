from api import PetFriends
from settings import valid_email, valid_password
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в тезультате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='Барбоскин', animal_type='двортерьер',
                                     age='4', pet_photo='images/cat1.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=5):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Еслди список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

        # Тест №1


def test_get_api_key(email=valid_email, password='666'):
    # запрос api ключа возвращает статус 403 при вводе неверного пароля

    status, result = pf.get_api_key(email, password)
    assert status == 403

    # Тест №2


def test_add_new_pet(name='Чейз', animal_type='такса',
                     age='-5', pet_photo='dachshund-1.jpg'):
    # Проверяем что нельзя добавить питомца с отрицательным возрастом

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 400

    # Тест №3


def test_add_new_pet_with_invalid_age(name='Дымок', animal_type='корелла',
                                      age='100500', pet_photo='uhod_i_soderjanie_korelli.jpg'):
    # Проверяем что нельзя добавить питомца с возрастом больше 1000 лет

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 400

    # Тест №4


def test_update_pet_info_with_invalid_age(name='Чейз', animal_type='Таксон', age=100500):
    # Проверяем отсутствие возможности обновления информации о питомце с возрастом больше 100500 лет

    auth_key = pf.get_api_key(valid_email, valid_password)
    my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        assert status == 400
    else:

        raise Exception("There is no my pets")


# Тест №5

def test_update_pet_info_with_negative_age(name='Дымка', animal_type='Попугай', age=-4):
    # Проверяем отсутствие возможности обновления информации о питомце с отрицательным возрастом

    auth_key = pf.get_api_key(valid_email, valid_password)
    my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        assert status == 400
    else:
        raise Exception("There is no my pets")

    # Тест №6


def test_update_pet_info_with_long_name(name='Дымкааааааааааааааааааааааааааааааааааааааа', animal_type='Попугай',
                                        age=4):
    # Проверяем отсутствие возможности обновления информации о питомце с именем более 20 символов

    auth_key = pf.get_api_key(valid_email, valid_password)
    my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        assert status == 400
    else:
        raise Exception("There is no my pets")


# Тест №7

def test_add_new_pet_with_long_name(name='Дымкааааааааааааааааааааааааааааааааааааааа', animal_type='Попугай',
                                    age='4', pet_photo='uhod_i_soderjanie_korelli.jpg'):
    # Проверяем что нельзя добавить питомца с именем длиннее 20 символов

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 400


# Тест №8

def test_add_photo_of_pet(pet_photo='dachshund-1.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    auth_key = pf.get_api_key(valid_email, valid_password)
    _, _ = pf.add_new_pet_simple(auth_key, 'КОТ', 'тайский', '7')

    my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    status, result = pf.add_photo_of_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)
    assert status == 200
    assert result['pet_photo'] != ''

    # Тест №9


def test_add_new_pet_simple_with_valid_data(name='Чейзон', animal_type='такса',
                                            age='5'):
    # Добавление питомца без фото

    auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name
    assert result['pet_photo'] == ''


# Тест №10

def test_add_new_pet_simple_without_name(animal_type='такса',
                                         age='5', pet_photo='dachshund-1.jpg'):
    # Добавление питомца без имени

    auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_simple(auth_key, animal_type, age, pet_photo)
    assert status == 200
    assert result['pet_photo'] == pet_photo
    assert result['name'] == ''
