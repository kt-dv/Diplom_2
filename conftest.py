import pytest
import requests
import random
import string
from urls import BASE_URL, REGISTER_ENDPOINT, USER_ENDPOINT


def generate_random_user():
    """Генерирует случайные данные для пользователя."""
    random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return {
        "email": f"{random_string}@test.ru",
        "password": "password123",
        "name": f"User_{random_string}"
    }


@pytest.fixture
def generate_random_user_fixture():
    return generate_random_user


@pytest.fixture
def created_user():
    """Создает пользователя до теста и удаляет его после."""
    user_data = generate_random_user()
    # Создаем пользователя
    response = requests.post(f"{BASE_URL}{REGISTER_ENDPOINT}", json=user_data)
    token = response.json().get("accessToken")

    yield user_data, token

    # Удаляем пользователя после теста
    if token:
        headers = {"Authorization": token}
        requests.delete(f"{BASE_URL}{USER_ENDPOINT}", headers=headers)


@pytest.fixture
def cleanup_user():
    """Генерирует данные для регистрации и удаляет пользователя после теста (если он создан)."""
    user_data = generate_random_user()
    yield user_data

    # Пытаемся залогиниться, чтобы получить токен для удаления
    login_response = requests.post(
        f"{BASE_URL}/api/auth/login",
        json={"email": user_data["email"], "password": user_data["password"]}
    )
    if login_response.status_code == 200:
        token = login_response.json().get("accessToken")
        if token:
            headers = {"Authorization": token}
            requests.delete(f"{BASE_URL}{USER_ENDPOINT}", headers=headers)