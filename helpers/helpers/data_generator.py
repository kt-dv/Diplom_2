import random
import string

def generate_random_user():
    random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return {
        "email": f"{random_string}@test.ru",
        "password": "password123",
        "name": f"User_{random_string}"
    }