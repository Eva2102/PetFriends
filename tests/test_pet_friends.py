import os
from api import PetFriends
from settings import valid_email, valid_password, nevalid_email, nevalid_password

pf = PetFriends()

def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result

def test_get_all_pets_with_valid_key(filter=""):
    _, auth_key = pf.get_api_key(valid_email,valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0


############## 10 тест-кейсов

# 1. Добавление питомца без фото
def test_add_pet_new_without_photo(name='Мяу', animal_type='Московская помоечная', age='5'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_inf_without_photo(auth_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name



# 2. Добавить фотографию питомца
def test_add_pet_new_photo(pet_photo='images/Cat.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    pet_id = my_pets['pets'][1]['id']

    status, result = pf.add_new_photo_pet(auth_key, pet_id, pet_photo)

    if len(my_pets['pets']) > 0:
        status, result = pf.add_new_photo_pet(auth_key, my_pets['pets'][1]['id'], pet_photo)
        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

        assert status == 200
        assert result['pet_photo'] == my_pets['pets'][1]['pet_photo']
    else:

        raise Exception("There is not my pets")


# 3. Проверяем запрос с валидным email и с невалидным password (negative test)
def test_get_api_key_for_user_invalid_password(email=valid_email, password=nevalid_password):
    status, result = pf.get_api_key(email, password)
    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    assert 'key' not in result


# 4. Проверяем запрос с невалидным email и с валидным password (negative test)
def test_get_api_key_for_user_invalid_email(email=nevalid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    assert 'key' not in result


# 5. Проверяем запрос с невалидным email и с невалидным password (negative test)
def test_get_api_key_for_user_invalid_email_pass(email=nevalid_email, password=nevalid_password):
    status, result = pf.get_api_key(email, password)
    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    assert 'key' not in result


# 6. Передаем пустое значение name при создании питомца (negative test)
def test_add_new_pet_with_empty_name(name='', animal_type='Московская помоечная', age='5', pet_photo='images/Cat.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    #  Питомец создается с пустым значением в name


# 7. В параметрах name передаем большое значение при создании питомца (negative test)
def test_add_new_pet_with_big_name(
        name='Richi кличка собаки. Чистокровный пес. Имеет 2 награды "Самый красивый пес 2021, 2022 годов. Любимец маленьких детей. Игривый, ласковый, верный защитник!!!',
        animal_type='немецкая овчарка', age='10', pet_photo='images/dog.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    # Питомец создан с большим количеством слов в имени


# 8. Добавление питомца сo спец.символами вместо букв в name (negative test)
def test_add_new_pet_with_name_characters(name='!@#$%^&&*()_+=?/.,`', animal_type='немецкая овчарка', age='10',
                                          pet_photo='images/dog.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    # Питомец создан с именем состоящим из спец.символов


# 9. В параметрах передадим отрицательный возраст при создании питомца (negative test)
def test_add_new_pet_negative_age(name='Richi', animal_type='немецкая овчарка', age='-3', pet_photo='images/dog.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    # Питомец создан с отрицательным возрастом


# 10. В параметрах передадим возраст больше 100 при создании питомца (negative test)
def test_add_new_pet_age_more(name='Richi', animal_type='немецкая овчарка', age='1000', pet_photo='images/dog.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
   #Питомец создан с возрастом 1000 лет


# 11. В параметрах передадим возраст буквами при создании питомца (negative test)
def test_add_pet_new_fail_letter_age(name='Вася', animal_type='кот', age='три'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_inf_without_photo(auth_key, name, animal_type, age)

    assert status == 200
   # Питомец добавлен с возрастом "три" вместо 3


# 12. Удалить чужого питомца (negative test)
def test_delete_another_pet():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, all_pets = pf.get_list_of_pets(auth_key, '')

    # Берём id любого питомца из списка и отправляем запрос на удаление
    pet_id = all_pets['pets'][10]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)
    # Ещё раз запрашиваем список своих питомцев
    _, all_pets = pf.get_list_of_pets(auth_key, '')

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    #Чужой питомец успешно удален


# 13. В параметрах передадим пустые значения при создании питомца (negative test)
def test_add_pet_new_fail_lempty_value(name='', animal_type='', age=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet_inf_without_photo(auth_key, name, animal_type, age)

    assert status == 200
     # Питомец добавлен с пустыми значениями





