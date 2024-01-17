import openai

from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')
client = openai.OpenAI(api_key=openai_api_key)

response = client.audio.speech.create(
    model="tts-1",
    voice="shimmer",
    input="Hello world! This is a streaming test.",
)

response.stream_to_file("output.mp3")


