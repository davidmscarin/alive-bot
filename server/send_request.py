import requests

def send_request(text_input, url = 'http://localhost:5000/message'):
    data = {'message': text_input}
    response = requests.post(url, json=data)
    print(response.json())

while True:
    send_request(text_input=input())
