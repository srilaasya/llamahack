from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access the API key using os.getenv
openai_api_key = os.getenv('OPENAI_API_KEY')

# Initialize OpenAI client
client = OpenAI(api_key=openai_api_key)

# Input audio file path from interface
#file_path = "/Users/laasya/Desktop/llamahack/output.mp3"

# Function takes in audio file and transcribes it


def transcribe_audio(mp3_content):

    # Open the audio file in binary mode
    with open('audio_file.mp3', "wb") as audio_file:
        audio_file.write(bytes(mp3_content))

    # Open the audio file in binary mode
    with open('audio_file.mp3', "rb") as audio_file:
        # Create transcription
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="text"
        )

    # Return the transcribed text
    return transcript


#print(transcribe_audio(file_path))
