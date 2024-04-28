# import requests

# url = 'http://localhost:8000/send_message'
# headers = {'Content-Type': 'application/json'}
# data = {'message': 'Hello, how are you?'}

# response = requests.post(url, json=data, headers=headers)
# if response.status_code == 200:
#     print("Response from server:", response.json())
# else:
#     print("Failed to get response:", response.text)


import requests

url = 'http://localhost:5000/message'
data = {'message': input()}

response = requests.post(url, json=data)
print(response.json())
