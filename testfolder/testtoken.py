import jwt
import requests

# get JWT token from /login route
routeurl = 'http://192.168.1.57:5000/'
credentials = {"username": "it21122", "password": "21122"}
response = requests.post(routeurl+"login", json=credentials)
data = response.json()
token = data["token"]
headers = {"Authorization": f"Bearer {token}"}

try:
    payload = jwt.decode(token, app.config['SECRET_KEY'], algorithm='HS256')
    print(payload)
except jwt.InvalidTokenError:
    print("Invalid token")