import requests
import pytest
import allure
from urls import BASE_URL, REGISTER_ENDPOINT

class TestUserCreation:

    @allure.title("Создание уникального пользователя")
    @allure.step("Создание уникального пользователя")
    def test_create_unique_user_success(self, cleanup_user):
        response = requests.post(f"{BASE_URL}{REGISTER_ENDPOINT}", json=cleanup_user)

        assert response.status_code == 200
        assert response.json().get("success") is True

    @allure.title("Создание пользователя, который уже существует (ошибка)")
    @allure.step("Создание пользователя, который уже существует (ошибка)")
    def test_create_existing_user_error(self, cleanup_user):
        # Создаем первого пользователя
        requests.post(f"{BASE_URL}{REGISTER_ENDPOINT}", json=cleanup_user)
        # Пытаемся создать дубль
        response = requests.post(f"{BASE_URL}{REGISTER_ENDPOINT}", json=cleanup_user)

        assert response.status_code == 403
        assert "User already exists" in response.text

    @allure.title("Создание пользователя без обязательного поля: {missing_field}")
    @allure.step("Создание пользователя без обязательного поля: {missing_field}")
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_create_user_missing_required_field(self, cleanup_user, missing_field):
        user_data = cleanup_user.copy()
        del user_data[missing_field]
        response = requests.post(f"{BASE_URL}{REGISTER_ENDPOINT}", json=user_data)

        assert response.status_code == 403
        assert "Email, password and name are required fields" in response.text