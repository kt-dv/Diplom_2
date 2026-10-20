import requests
import pytest

class TestUserCreation:
    def test_create_unique_user_success(self, base_url, generate_random_user):
        user_data = generate_random_user()
        response = requests.post(f"{base_url}/api/auth/register", json=user_data)
        assert response.status_code == 200
        assert response.json().get("success") is True

    def test_create_existing_user_error(self, base_url, generate_random_user):
        user_data = generate_random_user()
        requests.post(f"{base_url}/api/auth/register", json=user_data) # Создаем первого
        response = requests.post(f"{base_url}/api/auth/register", json=user_data) # Пытаемся создать дубль
        assert response.status_code == 403
        assert "User already exists" in response.text

    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_create_user_missing_required_field(self, base_url, generate_random_user, missing_field):
        user_data = generate_random_user()
        del user_data[missing_field]
        response = requests.post(f"{base_url}/api/auth/register", json=user_data)
        assert response.status_code == 403
        assert "Email, password and name are required fields" in response.text