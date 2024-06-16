from openai import OpenAI
from config import API_KEY, ASSISTANT_ID
client = OpenAI(api_key=API_KEY)
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import time
import re

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


def extract_coordinates(text):
    """
    Extracts coordinates from the text, assuming they are formatted as (latitude, longitude).
    """
    # Regex to find coordinates in the format (latitude, longitude)
    pattern = re.compile(r"\(([-+]?[0-9]*\.?[0-9]+),\s*([-+]?[0-9]*\.?[0-9]+)\)")
    match = pattern.search(text)
    if match:
        # Clean the text by removing the coordinates
        clean_text = pattern.sub("", text)
        coordinates = match.groups()
        return clean_text, coordinates
    return text, None

threads_arr = []

def create_empty_thread():
    """ Create an empty thread to initiate the conversation. """
    empty_thread = client.beta.threads.create()
    threads_arr.append(empty_thread.id)
    return empty_thread.id


@app.route('/threads', methods=['GET'])
@cross_origin()
def get_thread_list():
    print(threads_arr)
    return({'threads': threads_arr})

# @app.route('/threads/<thread_id>', method = ['GET'])
# def get_thread_messages(thread_id):
#     pass


@app.route('/message', methods=['POST'])
@cross_origin()
def send_and_receive_message():

    """
    Receives a message from a user, sends it to the OpenAI model within a thread,
    and returns the response from the assistant.
    """
    data = request.json
    user_input = data.get('message')
    new_thread = data.get('new_thread')
    specified_thread = str(data.get('thread_id'))
    print(f"received id: {specified_thread}")

    if new_thread:
        id = create_empty_thread()
        print(f"New thread created: {id}")
        
    if not new_thread:
        id = specified_thread
        print(f"Using thread {specified_thread}")
        

    extra_prompt = '''. If you mention a landmark, location, business or anything of the sort, include at the end of your response its latitude and longitude according to this regex pattern: "\(([-+]?[0-9]*\.?[0-9]+),\s*([-+]?[0-9]*\.?[0-9]+)\)"'''
    
    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    
    # Sending a message to the thread
    thread_message = client.beta.threads.messages.create(
        thread_id=id,
        role="user",
        content= user_input + extra_prompt
    )

    # Running the thread with the specific assistant
    run = client.beta.threads.runs.create(
        thread_id=id,
        assistant_id=ASSISTANT_ID
    )

    counter = 0
    #because the run would always be queued
    while run.status != "completed":
        run = client.beta.threads.runs.retrieve(thread_id=id, run_id=run.id)
        if counter % 10 == 0:
            print(f"\t\t{run}")
            counter += 1
            time.sleep(5)

    # Process and display messages
    thread_data = client.beta.threads.messages.list(thread_id=id).data

    # # Extract the assistant's last message from the response
    # last_message = thread_data[0].content[0].text.value
    # coords = extract_coordinates(last_message)

    # if coords:
    #     return ({"response": last_message, "coordinates": coords})
    
    # return {"response": last_message}

    last_message = thread_data[0]
    text, coords = extract_coordinates(last_message.content[0].text.value)
    role = last_message.role

    if coords:
        return ({"response": text, "coordinates": coords, "role": role})
    
    else:
        return({"response": text, "role": role})

if __name__ == '__main__':
    app.run(debug=True)
