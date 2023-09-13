from streamlit import *
from streamlit_chat import message
import requests

API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
API_TOKEN = "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"
headers = {"Authorization": f"Bearer {API_TOKEN}"}
header("🦁Hanyang University Chatbot")

if 'generated' not in session_state:
    session_state['generated'] = []

if 'past' not in session_state:
    session_state['past'] = []

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload) #Using API
	return response.json()


with form('form', clear_on_submit=True):
    user_input = text_input('You: ', '', key='input')
    submitted = form_submit_button('Send')

if submitted and user_input:
    output = query({
        "inputs": {
            "past_user_inputs": session_state.past,
            "generated_responses": session_state.generated,
            "text": user_input,
        },
        "parameters": {"repetition_penalty": 1.33},
    })

    session_state.generated.append(output["generated_text"])
    session_state.past.append(user_input)

if session_state['generated']:
    for i in range(len(session_state['generated'])-1, -1, -1):
        message(session_state["generated"][i], key=str(i))
        message(session_state['past'][i], is_user=True, key=str(i) + '_user')
