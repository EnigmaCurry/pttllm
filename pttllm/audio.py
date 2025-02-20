import numpy as np


def generate_silence(stream, voice, duration_sec):
    num_samples = int(duration_sec * voice.config.sample_rate)
    silence = np.zeros(num_samples, dtype=np.int16)
    stream.write(silence)

def say(stream, voice, text):
    for audio_chunk in voice.synthesize_stream_raw(text):
        audio_data = np.frombuffer(audio_chunk, dtype=np.int16)
        stream.write(audio_data)
