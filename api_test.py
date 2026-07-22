import requests

API_BASE = 'http://localhost:8000'
# Let's try to register a new user
register_data = {
    'full_name': 'Test User',
    'username': 'testuser123',
    'password': 'Password123'
}
res = requests.post(f"{API_BASE}/auth/register", json=register_data)
print("Register:", res.status_code, res.text)

# We need an admin to approve this user, but wait, if it's pending it will return 403, NOT 401!
login_data = {
    'username': 'testuser123',
    'password': 'Password123'
}
res = requests.post(f"{API_BASE}/auth/login", data=login_data)
print("Login before approve:", res.status_code, res.text)
