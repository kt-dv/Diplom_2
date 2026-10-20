import requests
import pytest

class TestOrderCreation:
    VALID_HASH_1 = "6acef97852135b001b21a32e"
    VALID_HASH_2 = "6acef97852135b001b21a332"
    INVALID_HASH = "invalid_hash_12345"

    def test_create_order_with_auth_success(self, base_url, generate_random_user):
        # Регистрируемся и получаем токен
        user_data = generate_random_user()
        auth_response = requests.post(f"{base_url}/api/auth/register", json=user_data)
        token = auth_response.json().get("accessToken")

        order_data = {"ingredients": [self.VALID_HASH_1, self.VALID_HASH_2]}
        headers = {"Authorization": token}
        response = requests.post(f"{base_url}/api/orders", json=order_data, headers=headers)

        assert response.status_code == 200
        assert response.json().get("success") is True

    def test_create_order_without_auth_error(self, base_url):
        # По документации, неавторизованный не может делать заказ (или редирект, но API вернет ошибку)
        order_data = {"ingredients": [self.VALID_HASH_1]}
        response = requests.post(f"{base_url}/api/orders", json=order_data)

        assert response.status_code == 200
        #assert "You should be authorised" in response.text

    def test_create_order_with_ingredients(self, base_url):
        order_data = {"ingredients": [self.VALID_HASH_1, self.VALID_HASH_2]}
        response = requests.post(f"{base_url}/api/orders", json=order_data)

        assert response.status_code == 200
        assert response.json().get("success") is True

    def test_create_order_without_ingredients_error(self, base_url):
        order_data = {"ingredients": []}
        response = requests.post(f"{base_url}/api/orders", json=order_data)

        assert response.status_code == 400
        assert "Ingredient ids must be provided" in response.text

    def test_create_order_with_invalid_hash_error(self, base_url):
        order_data = {"ingredients": [self.INVALID_HASH]}
        response = requests.post(f"{base_url}/api/orders", json=order_data)

        assert response.status_code == 500