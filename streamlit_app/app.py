import streamlit as st
import wave
import sys
import time
import pyaudio
import requests
import os

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1 if sys.platform == 'darwin' else 2
RATE = 44100
RECORD_SECONDS = 7

DATABASE_API_URL = os.getenv('DATABASE_API_URL')
BACKEND_API_URL = os.getenv('BACKEND_API_URL')

def transcribe_audio():
    # Send audio file to backend API for transcription
    with open('output.mp3', 'rb') as f:
        payload = f.read()
    headers = {
        'Content-Type': 'audio/mp3'
    }
    response = requests.post(f'{BACKEND_API_URL}process_audio', headers=headers, data=payload)
    if response.status_code == 200:
        transcript = response.content.decode('utf-8')
        st.write(transcript)
    else:
        st.write('Error transcribing audio')

def get_tasks():
    time.sleep(2)

def create_tasks():
    time.sleep(2)


state = st.session_state
state['audio_collected'] = False

audio_interface_container = st.empty()
if audio_interface_container.button('Get Started', use_container_width=True):
    #audio_interface_container.empty()
    #audio_interface_container = st.container()
    audio_interface_container.image('static/voice_visualizer.gif')
    #audio_interface_container.write('Listening...')
    with wave.open('output.mp3', 'wb') as wf:
        p = pyaudio.PyAudio()
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True)
        print('Recording...')
        for _ in range(0, RATE // CHUNK * RECORD_SECONDS):
            wf.writeframes(stream.read(CHUNK))
        print('Done')
        stream.close()
        p.terminate()
    audio_interface_container.empty()
    state['audio_collected'] = True
    # audio_interface_container.button('Process my Request', use_container_width=True)

if state['audio_collected']:
    with st.spinner("Processing your request..."):
        st.write("Transcribing audio...")
        transcribe_audio()
        st.write("Fetching Tasks...")
        get_tasks()
        st.write("Creating Tasks...")
        create_tasks()

# import plotly.express as px
# import pandas as pd
#
# df = pd.DataFrame([
#     dict(Task="Job A", Start='2009-01-01', Finish='2009-02-28'),
#     dict(Task="Job B", Start='2009-03-05', Finish='2009-04-15'),
#     dict(Task="Job C", Start='2009-02-20', Finish='2009-05-30')
# ])
#
# fig = px.timeline(df, x_start="Start", x_end="Finish", y="Task")
# fig.update_yaxes(autorange="reversed") # otherwise tasks are listed from the bottom up
# #fig.show()
#
# st.write(fig)

# from st_audiorec import st_audiorec
#
# wav_audio_data = st_audiorec()
#
# if wav_audio_data is not None:
#     st.audio(wav_audio_data, format='audio/wav')

# from streamlit_mic_recorder import mic_recorder, speech_to_text
#
#
#
#
# state=st.session_state
#
# if 'text_received' not in state:
#     state.text_received=[]
#
# c1,c2=st.columns(2)
# with c1:
#     st.write("Convert speech to text:")
# with c2:
#     text=speech_to_text(language='en',use_container_width=True,just_once=True,key='STT')
#
# if text:
#     state.text_received.append(text)
#
# for text in state.text_received:
#     st.text(text)
#
# st.write("Record your voice, and play the recorded audio:")
# audio=mic_recorder(start_prompt="⏺️",stop_prompt="⏹️",key='recorder')
#
# if audio:
#     st.audio(audio['bytes'])

# from audiorecorder import audiorecorder
#
# # https://github.com/theevann/streamlit-audiorecorder
# audio = audiorecorder('Talk to Me', 'Stop Listening')
# if len(audio) > 0:
#     # To save audio to a file, use pydub export method:
#     audio.export('audio.mp3', format="wav")