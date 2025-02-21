import numpy as np
import sounddevice as sd
from pprint import pprint
from thefuzz import process

def get_interface(name, input=False, threshold=60):
    """Get the audio interface by name using fuzzy matching"""
    devices = sd.query_devices()
    if input:
        names = [d['name'] for d in devices if d['max_input_channels'] > 0]
    else:
        names = [d['name'] for d in devices if d['max_output_channels'] > 0]

    # Use thefuzz to find the closest match with a similarity score
    match, score = process.extractOne(name, names)

    if score >= threshold:
        return match
    else:
        raise ValueError(f"No matching audio interface found for '{name}'. Closest match '{match}' scored {score}%.")

def generate_silence(stream, voice, duration_sec):
    num_samples = int(duration_sec * voice.config.sample_rate)
    silence = np.zeros(num_samples, dtype=np.int16)
    stream.write(silence)

def say(stream, voice, text):
    for audio_chunk in voice.synthesize_stream_raw(text):
        audio_data = np.frombuffer(audio_chunk, dtype=np.int16)
        stream.write(audio_data)
