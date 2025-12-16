import pytest
import requests
import allure
from data import INGREDIENTS_ENDPOINT, ORDERS_ENDPOINT, AUTH_REQUIRED_MESSAGE, INGREDIENTS_REQUIRED_MESSAGE

class TestIngredients:
    @allure.title("Получение списка ингредиентов")
    def test_get_ingredients(self):
        with allure.step("Запрос списка ингредиентов"):
            response = requests.get(INGREDIENTS_ENDPOINT)
            
        with allure.step("Проверка ответа"):
            assert response.status_code == 200
            response_data = response.json()
            assert response_data["success"] is True
            assert "data" in response_data
            
            data = response_data["data"]
            assert isinstance(data, list)
            assert len(data) > 0
            
            types = {item["type"] for item in data}
            assert "bun" in types
            assert "sauce" in types
            assert "main" in types

class TestOrders:
    @allure.title("Создание заказа с авторизацией и ингредиентами")
    def test_create_order_authorized_with_ingredients(self, auth_token, ingredients_data):
        ingredients = [
            ingredients_data["bun"][0],
            ingredients_data["sauce"][0],
            ingredients_data["main"][0]
        ]
        
        headers = {"Authorization": auth_token}
        
        with allure.step("Создание заказа с ингредиентами"):
            response = requests.post(ORDERS_ENDPOINT, json={"ingredients": ingredients}, headers=headers)
            
        with allure.step("Проверка успешного создания"):
            assert response.status_code == 200
            response_data = response.json()
            assert response_data["success"] is True
            assert "name" in response_data
            assert "order" in response_data

    @allure.title("Создание заказа без авторизации")
    def test_create_order_unauthorized(self, ingredients_data):
        ingredients = [ingredients_data["bun"][0]]
        
        with allure.step("Создание заказа без авторизации"):
            response = requests.post(ORDERS_ENDPOINT, json={"ingredients": ingredients})
            
        with allure.step("Проверка ошибки авторизации"):
            assert response.status_code == 401
            response_data = response.json()
            assert response_data["success"] is False
            assert response_data["message"] == AUTH_REQUIRED_MESSAGE

    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_no_ingredients(self, auth_token):
        headers = {"Authorization": auth_token}
        
        with allure.step("Создание заказа без ингредиентов"):
            response = requests.post(ORDERS_ENDPOINT, json={"ingredients": []}, headers=headers)
            
        with allure.step("Проверка ошибки отсутствия ингредиентов"):
            assert response.status_code == 400
            response_data = response.json()
            assert response_data["success"] is False
            assert response_data["message"] == INGREDIENTS_REQUIRED_MESSAGE

    @allure.title("Создание заказа с неверными ингредиентами")
    def test_create_order_invalid_ingredients(self, auth_token):
        headers = {"Authorization": auth_token}
        
        with allure.step("Создание заказа с неверными ингредиентами"):
            response = requests.post(ORDERS_ENDPOINT, 
                                   json={"ingredients": ["invalid_hash_123", "another_invalid"]},
                                   headers=headers)
            
        with allure.step("Проверка ошибки сервера"):
            assert response.status_code == 500
