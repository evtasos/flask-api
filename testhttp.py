import requests

url = "http://127.0.0.1:5000/upload"
file_path = r"C:\Users\plhroforikh-1\Desktop\thesis\flask-api\filespdf\testflask.docx"

with open(file_path, 'rb') as f:
    file = {'file': (file_path, f)}
    response = requests.post(url, files=file)

print(response.json())