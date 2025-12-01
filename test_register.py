import requests

url = "http://127.0.0.1:8000/auth/register"
data = {
    "username": "testuser",
    "email": "testuser@example.com",
    "password": "testpassword"
}

try:
    response = requests.post(url, json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")
