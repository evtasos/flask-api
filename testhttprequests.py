import requests

# # upload
# url = "http://127.0.0.1:5000/upload"
# file_path = r"C:\Users\Me\Desktop\THESIS\ipsum.docx"
# with open(file_path, 'rb') as f:
#     file = {'file': (file_path, f)}
#     response = requests.post(url, files=file)

#list
# response = requests.get("http://127.0.0.1:5000/list")

#delete
response = requests.delete("http://127.0.0.1:5000/delete/test2.pdf")

# #create
# data = {
#     "template": "ipsum.docx",
#     "recipient": "etasos",
#     "am": 21122,
#     "year": 2023
# }
# response = requests.post("http://127.0.0.1:5000/create", json=data)

# # download
# response = requests.get("http://127.0.0.1:5000/download/ipsum.docx")

print(response.json())

