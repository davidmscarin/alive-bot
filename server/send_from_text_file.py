import requests

def extract_text_from_file(filename):
    texts = []
    current_text = []

    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line:  # If the line is not empty
                current_text.append(line)
            elif current_text:  # If the line is empty and we have text accumulated
                texts.append('\n'.join(current_text))
                current_text = []  # Reset current_text for the next text block
        
        # Append the last text block if the file doesn't end with a blank line
        if current_text:
            texts.append('\n'.join(current_text))
    
    return texts

texts = extract_text_from_file('questions.txt')

def send_request(text_input, url = 'http://localhost:5000/message'):
    data = {'message': text_input}
    response = requests.post(url, json=data)
    print(response.json())

for line in texts:
    print(f'User:\n{line}\nModel:\n')
    send_request(text_input=line)
    print('\n')

