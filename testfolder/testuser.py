import requests, jwt


# # get JWT token from /login route
# routeurl = 'http://192.168.1.57:5000/'
# credentials = {"username": "it21122", "password": "21122"}
# response = requests.post("http://192.168.1.57:5000/login", json=credentials)
# data = response.json()
# token = data["token"]
# print('1',token)
# # Strip "Bearer " prefix from token
# secret_key = 'ecWP1fNMQu'
# # token = token.split(" ")[1]
# try:
#     # Decode the token and check for any errors
#     payload = jwt.decode(token, secret_key, algorithm='HS256')
#     headers = {"Authorization": f"Bearer {token}"}
#     print('2',payload)
# except jwt.ExpiredSignatureError:
#     print("Token expired")
# except jwt.InvalidTokenError:
#     print("Invalid token")
payload = {'username': 'it21122'}
SECRET_KEY = '131231312'
token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
print(token)


try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    print(payload)
        

except jwt.ExpiredSignatureError as e:
    print(e, ({"error1": "Token expired"}), 401)
except jwt.InvalidTokenError as e:
    print(e)
    print(({"error2": "Invalid token"}), 402)