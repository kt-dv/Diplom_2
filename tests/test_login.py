import requests
import pytest
import allure
from urls import BASE_URL, LOGIN_ENDPOINT

class TestLogin:

    @allure.title("Логин существующего пользователя")
    @allure.step("Логин существующего пользователя")
    def test_login_existing_user_success(self, created_user):
        user_data, _ = created_user
        login_data = {"email": user_data["email"], "password": user_data["password"]}
        response = requests.post(f"{BASE_URL}{LOGIN_ENDPOINT}", json=login_data)

        assert response.status_code == 200
        assert response.json().get("success") is True

    @allure.title("Логин с неверными учетными данными: {wrong_field}")
    @allure.step("Логин с неверными учетными данными: {wrong_field}")
    @pytest.mark.parametrize("wrong_field", ["email", "password"])
    def test_login_wrong_credentials(self, created_user, wrong_field):
        user_data, _ = created_user
        login_data = {"email": user_data["email"], "password": user_data["password"]}
        login_data[wrong_field] = "wrong_data_123"
        response = requests.post(f"{BASE_URL}{LOGIN_ENDPOINT}", json=login_data)

        assert response.status_code == 401
        assert "email or password are incorrect" in response.text