import streamlit as st
import streamlit.components.v1 as components
import requests
import json
import pygame

CHUNK_SIZE = 1024  # Size of chunks to read/write at a time
XI_API_KEY = st.secrets["labs_api_key"]  # Your API key for authentication
VOICE_ID = "XB0fDUnXU5powFXDhCwa"  # ID of the voice model to use
# Text you want to convert to speech
# TEXT_TO_SPEAK = "text"
OUTPUT_PATH = "output.mp3"

with open('style.css') as f:
    css = f.read()
st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)


# Displaying logos at the top
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.image("royaume_du_maroc_logo.png", width=200, output_format='auto')

with col5:
    st.image("logo_pmp.png", width=75, output_format='auto')


st.title("المساعد الخاص برئاسة النيابة العامة")

# API configuration
url = 'https://www.chatbase.co/api/v1/chat'
headers = {
    # Replace <API-KEY> with your actual API key
    'Authorization': 'Bearer '+st.secrets["chatbase_api_key"],
    'Content-Type': 'application/json'
}

# Check and initialize session state variables
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


def send_message(text):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Preparing data for the new API
    data = {
        "messages": [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
        # Replace <Chatbot-ID> with your actual Chatbot ID
        "chatbotId": "vaWO65hVvRo2NLzhDF6mu",
        "stream": False,
        "temperature": 0
    }

    # Sending the request to the new API
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        json_data = response.json()
        assistant_message = json_data['text']
    else:
        json_data = response.json()
        assistant_message = "Error: " + \
            json_data.get('message', 'Failed to fetch response.')

    # Displaying the response from the assistant
    with st.chat_message("assistant"):
        st.markdown(assistant_message)
        tts_url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}/stream"

    # Set up headers for the API request, including the API key for authentication
    headers = {
        "Accept": "application/json",
        "xi-api-key": XI_API_KEY
    }

    # Set up the data payload for the API request, including the text and voice settings
    data = {
        "text": assistant_message,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.8,
            "style": 0.0,
            "use_speaker_boost": True
        }
    }

    # Make the POST request to the TTS API with headers and data, enabling streaming response
    response = requests.post(tts_url, headers=headers, json=data, stream=True)

    # Check if the request was successful
    if response.ok:
        # Open the output file in write-binary mode
        with open(OUTPUT_PATH, "wb") as f:
            # Read the response in chunks and write to the file
            for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                f.write(chunk)
        st.audio("output.mp3", format="audio/mp3", start_time=0)
    else:
        # Print the error message if the request was not successful
        print(response.text)

    st.session_state.messages.append(
        {"role": "assistant", "content": assistant_message})


if len(st.session_state.messages) == 0:
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Hi"):
            send_message("Hi")
    with col2:
        if st.button("Help"):
            send_message("Help")
    with col3:
        if st.button("More Info"):
            send_message("More Info")

# Input from user
if prompt := st.chat_input("أهلاً! بماذا يمكنني مساعدتك؟"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Preparing data for the new API
    data = {
        "messages": [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
        # Replace <Chatbot-ID> with your actual Chatbot ID
        "chatbotId": "vaWO65hVvRo2NLzhDF6mu",
        "stream": False,
        "temperature": 0
    }

    # Sending the request to the new API
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        json_data = response.json()
        assistant_message = json_data['text']
    else:
        json_data = response.json()
        assistant_message = "Error: " + \
            json_data.get('message', 'Failed to fetch response.')

    # Displaying the response from the assistant
    with st.chat_message("assistant"):
        st.markdown(assistant_message)
        tts_url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}/stream"

    # Set up headers for the API request, including the API key for authentication
    headers = {
        "Accept": "application/json",
        "xi-api-key": XI_API_KEY
    }

    # Set up the data payload for the API request, including the text and voice settings
    data = {
        "text": assistant_message,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.8,
            "style": 0.0,
            "use_speaker_boost": True
        }
    }

    # Make the POST request to the TTS API with headers and data, enabling streaming response
    response = requests.post(tts_url, headers=headers, json=data, stream=True)

    # Check if the request was successful
    if response.ok:
        # Open the output file in write-binary mode
        with open(OUTPUT_PATH, "wb") as f:
            # Read the response in chunks and write to the file
            for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                f.write(chunk)
        st.audio("output.mp3", format="audio/mp3", start_time=0)
    else:
        # Print the error message if the request was not successful
        print(response.text)

    st.session_state.messages.append(
        {"role": "assistant", "content": assistant_message})
