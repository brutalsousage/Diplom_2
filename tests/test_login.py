import pytest
import requests
import allure
from data import LOGIN_ENDPOINT, INVALID_CREDENTIALS_MESSAGE

class TestLogin:
    @allure.title("Успешный вход в систему")
    def test_login_successful(self, registered_user):
        payload = {
            "email": registered_user["email"],
            "password": registered_user["password"]
        }
        
        with allure.step("Запрос на вход"):
            response = requests.post(LOGIN_ENDPOINT, json=payload)
            
        with allure.step("Проверка успешного входа"):
            assert response.status_code == 200
            response_data = response.json()
            assert response_data["success"] is True
            assert "accessToken" in response_data
            assert response_data["accessToken"].startswith("Bearer ")
            assert "refreshToken" in response_data
            assert response_data["user"]["email"] == registered_user["email"]
            assert response_data["user"]["name"] == registered_user["name"]

    @pytest.mark.parametrize("invalid_data", [
        {"email": "", "password": "validpass"},
        {"email": "valid@email.com", "password": ""},
        {"email": "invalid@email.com", "password": "wrongpass"},
    ])
    @allure.title("Вход с неверными данными: {invalid_data}")
    def test_login_invalid(self, invalid_data):
        with allure.step("Запрос на вход с неверными данными"):
            response = requests.post(LOGIN_ENDPOINT, json=invalid_data)
            
        with allure.step("Проверка ошибки авторизации"):
            assert response.status_code == 401
            response_data = response.json()
            assert response_data["success"] is False
            assert response_data["message"] == INVALID_CREDENTIALS_MESSAGE
