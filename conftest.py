import pytest
import requests
import allure
from faker import Faker
from data import REGISTER_ENDPOINT, LOGIN_ENDPOINT

fake = Faker()

@pytest.fixture
@allure.step("Генерация данных нового пользователя")
def new_user_data():
    email = fake.user_name() + "@yandex.ru"
    password = fake.password(length=10)
    name = fake.name()[:10]
    
    return {
        "email": email,
        "password": password,
        "name": name
    }

@pytest.fixture
@allure.step("Создание зарегистрированного пользователя")
def registered_user():
    email = fake.user_name() + "@yandex.ru"
    password = fake.password(length=10)
    name = fake.name()[:50]
    
    with allure.step("Регистрация пользователя"):
        payload = {"email": email, "password": password, "name": name}
        requests.post(REGISTER_ENDPOINT, json=payload)
    
    return {"email": email, "password": password, "name": name}

@pytest.fixture
@allure.step("Получение токена авторизации")
def auth_token(registered_user):
    with allure.step("Логин пользователя"):
        payload = {
            "email": registered_user["email"],
            "password": registered_user["password"]
        }
        response = requests.post(LOGIN_ENDPOINT, json=payload)
        return response.json()["accessToken"]

@pytest.fixture
@allure.step("Получение данных об ингредиентах")
def ingredients_data():
    from data import INGREDIENTS_ENDPOINT
    with allure.step("Получение списка ингредиентов"):
        response = requests.get(INGREDIENTS_ENDPOINT)
        response_data = response.json()
        
        data = response_data["data"]
        return {
            "bun": [item["_id"] for item in data if item["type"] == "bun"],
            "sauce": [item["_id"] for item in data if item["type"] == "sauce"],
            "main": [item["_id"] for item in data if item["type"] == "main"]
        }
