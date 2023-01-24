import requests

# get JWT token from /login route
credentials = {"username": "etasos", "password": "test1234"}
response = requests.post("http://192.168.1.57:5000/login", json=credentials)
data = response.json()
token = data["token"]
headers = {"Authorization": f"Bearer {token}"}
print(token)
request_type = input("Enter request type (upload, list, delete, create, download): ")

if request_type == "upload":
    # upload
    url = "http://192.168.1.57:5000/upload"
    with open("ipsum.docx", 'rb') as f:
        response = requests.post(url, files={'file': f},headers=headers)
elif request_type == "list":
    # list
    response = requests.get("http://192.168.1.57:5000/list")
elif request_type == "delete":
    #delete
    response = requests.delete("http://192.168.1.57:5000/delete/lorem_etasos_14-01-2023.docx")
elif request_type == "create":
    #create
    data = {
        "template": "lorem.docx",
        "recipient": "etasos",
        "am": 21122,
        "year": 2023
    }
    response = requests.post("http://192.168.1.57:5000/create", json=data, headers=headers)
    
    # # download
    # response = requests.get("http://127.0.0.1:5000/download/ipsum.docx")

print(response.json())

