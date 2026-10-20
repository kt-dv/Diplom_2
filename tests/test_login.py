import requests
import pytest

class TestLogin:
    def test_login_existing_user_success(self, base_url, generate_random_user):
        user_data = generate_random_user()
        requests.post(f"{base_url}/api/auth/register", json=user_data)

        login_data = {"email": user_data["email"], "password": user_data["password"]}
        response = requests.post(f"{base_url}/api/auth/login", json=login_data)
        assert response.status_code == 200
        assert response.json().get("success") is True

    @pytest.mark.parametrize("wrong_field", ["email", "password"])
    def test_login_wrong_credentials(self, base_url, generate_random_user, wrong_field):
        user_data = generate_random_user()
        requests.post(f"{base_url}/api/auth/register", json=user_data)

        login_data = {"email": user_data["email"], "password": user_data["password"]}
        login_data[wrong_field] = "wrong_data_123"

        response = requests.post(f"{base_url}/api/auth/login", json=login_data)
        assert response.status_code == 401
        assert "email or password are incorrect" in response.text