from openai import OpenAI
from config import API_KEY, ASSISTANT_ID
client = OpenAI(api_key=API_KEY)
from flask import Flask, request, jsonify
import time

app = Flask(__name__)

def create_empty_thread():
    """ Create an empty thread to initiate the conversation. """
    empty_thread = client.beta.threads.create()
    return empty_thread.id

empty_thread_id = create_empty_thread()

@app.route('/message', methods=['POST'])
def send_and_receive_message(id = empty_thread_id):

    """
    Receives a message from a user, sends it to the OpenAI model within a thread,
    and returns the response from the assistant.
    """
    data = request.json
    user_input = data.get('message')
    extra_prompt = '''. If you mention a landmark, location, business or anything of the sort, include at the end of your response its latitude and longitude according to this regex pattern: "\(([-+]?[0-9]*\.?[0-9]+),\s*([-+]?[0-9]*\.?[0-9]+)\)"'''
    
    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    
    # Sending a message to the thread
    thread_message = client.beta.threads.messages.create(
        id,
        role="user",
        content= user_input + extra_prompt
    )

    # Running the thread with the specific assistant
    run = client.beta.threads.runs.create(
        id,
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
    thread_data = client.beta.threads.messages.list(id).data

    # Extract the assistant's last message from the response
    last_message = thread_data[-1].content[0].text.value

    return ({"response": last_message})

if __name__ == '__main__':
    app.run(debug=True)
