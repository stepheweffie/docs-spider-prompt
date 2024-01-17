import simpleaudio as sa
from pydub import AudioSegment
import io
import requests
import wave


def play_mp3(file_path):
    # Handle both local and remote files
    if file_path.startswith("http://") or file_path.startswith("https://"):
        # If it's a remote file, download it
        response = requests.get(file_path)
        audio_data = io.BytesIO(response.content)
        audio = AudioSegment.from_file(audio_data, format="mp3")
    else:
        # If it's a local file, load it directly
        audio = AudioSegment.from_file(file_path, format="mp3")

    # Convert to WAV format
    audio = audio.set_frame_rate(44100).set_channels(2)
    wav_io = io.BytesIO()
    audio.export(wav_io, format="wav")
    wav_io.seek(0)

    # Play the audio
    wave_obj = sa.WaveObject.from_wave_read(wave.open(wav_io, 'rb'))
    play_obj = wave_obj.play()
    play_obj.wait_done()  # Wait until sound has finished playing


# Replace 'path_to_your_mp3_file.mp3' with the path to your MP3 file
play_mp3('output.mp3')
