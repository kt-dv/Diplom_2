import requests
import pytest
import allure
from urls import BASE_URL, ORDERS_ENDPOINT, VALID_HASH_1, VALID_HASH_2, INVALID_HASH

class TestOrderCreation:

    @allure.title("Создание заказа с авторизацией")
    @allure.step("Создание заказа с авторизацией")
    def test_create_order_with_auth_success(self, created_user):
        _, token = created_user
        order_data = {"ingredients": [VALID_HASH_1, VALID_HASH_2]}
        headers = {"Authorization": token}
        response = requests.post(f"{BASE_URL}{ORDERS_ENDPOINT}", json=order_data, headers=headers)

        assert response.status_code == 200
        assert response.json().get("success") is True

    @allure.title("Создание заказа без авторизации")
    @allure.step("Создание заказа без авторизации")
    def test_create_order_without_auth_error(self):
        order_data = {"ingredients": [VALID_HASH_1]}
        response = requests.post(f"{BASE_URL}{ORDERS_ENDPOINT}", json=order_data)

        assert response.status_code == 200
        assert response.json()["success"] is True

    @allure.title("Создание заказа с ингредиентами")
    @allure.step("Создание заказа с ингредиентами")
    def test_create_order_with_ingredients(self):
        order_data = {"ingredients": [VALID_HASH_1, VALID_HASH_2]}
        response = requests.post(f"{BASE_URL}{ORDERS_ENDPOINT}", json=order_data)

        assert response.status_code == 200
        assert response.json().get("success") is True

    @allure.title("Создание заказа без ингредиентов (ошибка)")
    @allure.step("Создание заказа без ингредиентов (ошибка)")
    def test_create_order_without_ingredients_error(self):
        order_data = {"ingredients": []}
        response = requests.post(f"{BASE_URL}{ORDERS_ENDPOINT}", json=order_data)

        assert response.status_code == 400
        assert "Ingredient ids must be provided" in response.text

    @allure.title("Создание заказа с неверным хешем (ошибка)")
    @allure.step("Создание заказа с неверным хешем (ошибка)")
    def test_create_order_with_invalid_hash_error(self):
        order_data = {"ingredients": [INVALID_HASH]}
        response = requests.post(f"{BASE_URL}{ORDERS_ENDPOINT}", json=order_data)

        assert response.status_code == 500