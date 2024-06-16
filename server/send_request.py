import requests

def send_message(text_input,  new_thread, thread_id, url = 'http://localhost:5000/message'):
    data = {'message': text_input, 'new_thread': new_thread, 'thread_id': thread_id}
    response = requests.post(url, json=data)
    print(response.json())

def get_threads(url = 'http://localhost:5000/threads'):
    thread_arr = requests.get(url)
    print(thread_arr.json())


send_message(text_input="hello. What is my name?", new_thread= True, thread_id="thread_RiBQM7TjEJs0IORTs4h7VUJw")
get_threads()