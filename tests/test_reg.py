import pytest
import requests
import allure
from data import REGISTER_ENDPOINT, REQUIRED_FIELDS_MESSAGE, USER_EXISTS_MESSAGE

class TestUserCreation:
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    @allure.title("Создание пользователя без обязательного поля: {missing_field}")
    def test_create_user_missing_required_field(self, new_user_data, missing_field):
        payload = new_user_data.copy()
        del payload[missing_field]
        
        with allure.step("Отправка запроса без обязательного поля"):
            response = requests.post(REGISTER_ENDPOINT, json=payload)
            
        with allure.step("Проверка ответа"):
            assert response.status_code == 403
            response_data = response.json()
            assert response_data["success"] is False
            assert response_data["message"] == REQUIRED_FIELDS_MESSAGE

    @allure.title("Создание уникального пользователя")
    def test_create_unique_user(self, new_user_data):
        with allure.step("Отправка запроса на создание пользователя"):
            response = requests.post(REGISTER_ENDPOINT, json=new_user_data)
            
        with allure.step("Проверка успешного создания"):
            assert response.status_code == 200
            response_data = response.json()
            assert response_data["success"] is True

    @allure.title("Создание уже существующего пользователя")
    def test_create_existing_user(self, new_user_data):
        with allure.step("Первая регистрация пользователя"):
            first_response = requests.post(REGISTER_ENDPOINT, json=new_user_data)
            assert first_response.status_code == 200
            
        with allure.step("Повторная регистрация того же пользователя"):
            second_response = requests.post(REGISTER_ENDPOINT, json=new_user_data)
            
        with allure.step("Проверка ошибки дублирования"):
            assert second_response.status_code == 403
            response_data = second_response.json()
            assert response_data["success"] is False
            assert response_data["message"] == USER_EXISTS_MESSAGE
