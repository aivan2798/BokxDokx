import os,io
import numpy as np
from openai import OpenAI
import riva.client
from dotenv import load_dotenv
import streamlit as st
from streamlit_mic_recorder import mic_recorder

# access the environment variables from the .env file
load_dotenv()

TTS_GRPC_ENDPOINT = os.environ.get('TTS_GRPC_ENDPOINT')
OVH_AI_ENDPOINTS_URL = os.environ.get('OVH_AI_ENDPOINTS_URL')
OVH_AI_ENDPOINTS_ACCESS_TOKEN = os.environ.get('OVH_AI_ENDPOINTS_ACCESS_TOKEN')

oai_client = OpenAI(
    base_url=OVH_AI_ENDPOINTS_URL,
    api_key=OVH_AI_ENDPOINTS_ACCESS_TOKEN
)

tts_client = riva.client.SpeechSynthesisService(
    riva.client.Auth(
        uri=TTS_GRPC_ENDPOINT,
        use_ssl=True,
        metadata_args=[["authorization", f"bearer {OVH_AI_ENDPOINTS_ACCESS_TOKEN}"]]
    )
)

def xasr_transcription(question, oai_client):
    # Assume 'audio_bytes' is your stream data
    buffer = io.BytesIO(question)
    buffer.name = "audio.wav"
    return oai_client.audio.transcriptions.create(
        model="whisper-large-v3",
        file=buffer
    ).text

def asr_transcription(question, oai_client):
    # Use 'with' to ensure the buffer is closed as soon as the block ends
    with io.BytesIO(question) as buffer:
        buffer.name = "audio.wav"
        response = oai_client.audio.transcriptions.create(
            model="whisper-large-v3", # Change to whisper-1 for official OpenAI API
            file=buffer
        )
        return response.text

def llm_answer(input, oai_client):
    response = oai_client.chat.completions.create(
                model="Mixtral-8x7B-Instruct-v0.1", 
                messages=input,
                temperature=0,
                max_tokens=1024,
            )
    msg = response.choices[0].message.content

    return msg

def tts_synthesis(response, tts_client):

    # set up config
    sample_rate_hz = 48000
    req = {
            "language_code"  : "en-US",                           # languages: en-US
            "encoding"       : riva.client.AudioEncoding.LINEAR_PCM ,
            "sample_rate_hz" : sample_rate_hz,                    # sample rate: 48KHz audio
            "voice_name"     : "English-US.Female-1"              # voices: `English-US.Female-1`, `English-US.Male-1`
    }

    # return response
    req["text"] = response
    synthesized_response = tts_client.synthesize(**req)

    return np.frombuffer(synthesized_response.audio, dtype=np.int16), sample_rate_hz


# streamlit interface
with st.container():
    st.title("💬 Audio Virtual Assistant Chatbot")

with st.container(height=600):
    messages = st.container()

    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "system", "content": "Hello, I'm AVA!", "avatar":"🤖"}]

    for msg in st.session_state.messages:
        messages.chat_message(msg["role"], avatar=msg["avatar"]).write(msg["content"])
# File uploader widget restricting to wav files
uploaded_file = st.file_uploader("Choose a WAV file", type="wav")

if uploaded_file is not None:
    # Display audio player
    st.audio(uploaded_file, format="audio/wav")
    
    # Example: Accessing file data
    st.write("Filename:", uploaded_file.name)

with st.container():

    placeholder = st.empty()
    _, recording = placeholder.empty(), mic_recorder(
            start_prompt="START RECORDING YOUR QUESTION ⏺️", 
            stop_prompt="STOP ⏹️", 
            format="wav",
            use_container_width=True,
            key='recorder'
    )

    if True:#recording:  
        print("recording...")
        #with open("spoken.wav","wb") as spoken:
        #    spoken.write(recording['bytes'])
        
        spoken = open("call.wav","rb")
        recorded = spoken.read()
        #user_question = asr_transcription(recording['bytes'], oai_client)
        user_question = asr_transcription(recorded, oai_client)
        print("asked transcription: ",user_question)
        if prompt := user_question:
            st.session_state.messages.append({"role": "user", "content": prompt, "avatar":"👤"})
            messages.chat_message("user", avatar="👤").write(prompt)
            msg = llm_answer(st.session_state.messages, oai_client)
            st.session_state.messages.append({"role": "assistant", "content": msg, "avatar": "🤖"})
            messages.chat_message("system", avatar="🤖").write(msg)

            if msg is not None:
                audio_samples, sample_rate_hz = tts_synthesis(msg, tts_client)
                placeholder.audio(audio_samples, sample_rate=sample_rate_hz, autoplay=True)