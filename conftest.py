import pytest
import random
import string

BASE_URL = "https://qa-stellarburgers.education-services.ru"

@pytest.fixture
def base_url():
    return BASE_URL

@pytest.fixture
def generate_random_user():
    def _generate():
        random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        email = f"{random_string}@test.ru"
        password = "password123"
        name = f"User_{random_string}"
        return {"email": email, "password": password, "name": name}
    return _generate