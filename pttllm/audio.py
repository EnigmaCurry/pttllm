import numpy as np
import sounddevice as sd
from pprint import pprint
from thefuzz import process
from scipy.signal import resample_poly
from .ptt import ptt_on, ptt_off

def get_interface(name):
    """Get the audio interface by name"""
    devices = sd.query_devices()

    for device in devices:
        if device['name'] == name:
            return device
    else:
        raise ValueError(f"No matching audio interface found for '{name}'. Available devices: {[d['name'] for d in devices]}")

def list_interfaces():
    """List all audio interfaces"""
    devices = sd.query_devices()

    # Build a list of (index, name) tuples for all devices
    device_list = [(idx, d['name']) for idx, d in enumerate(devices)]

    print("Available devices:")
    for device in device_list:
        print(f"  {device[1]}")

def validate_device(device_index, samplerate, channels):
    try:
        info = sd.query_devices(device_index)
        supported_samplerate = sd.check_output_settings(
            device=device_index,
            samplerate=samplerate,
            channels=channels
        )
        print(f"Device '{info['name']}' supports {channels} channels at {samplerate} Hz.")
    except Exception as e:
        print(f"Device validation failed: {e}")
        return False
    return True

def generate_silence(stream, voice, duration_sec):
    num_samples = int(duration_sec * stream.samplerate)
    silence = np.zeros(num_samples, dtype=np.int16)
    if stream.channels > 1:
        # Duplicate silence across all channels
        silence = np.repeat(silence[:, np.newaxis], stream.channels, axis=1)
    stream.write(silence)

def say(stream, voice, text, transmit=True):
    try:
        if transmit:
            ptt_on()

        for audio_chunk in voice.synthesize_stream_raw(text):
            audio_data = np.frombuffer(audio_chunk, dtype=np.int16)

            # Resample using resample_poly for stability
            if voice.config.sample_rate != stream.samplerate:
                gcd = np.gcd(int(voice.config.sample_rate), int(stream.samplerate))
                up = stream.samplerate // gcd
                down = voice.config.sample_rate // gcd

                print(f"Resampling: up={up}, down={down}, original_length={len(audio_data)}")
                audio_data = resample_poly(audio_data, up, down).astype(np.int16)
                print(f"Resampled length: {len(audio_data)}")

            # Handle mono to stereo if needed
            if stream.channels == 2 and audio_data.ndim == 1:
                audio_data = np.repeat(audio_data[:, np.newaxis], 2, axis=1)

            # Ensure correct data type and shape before writing
            assert audio_data.dtype == np.int16, "Audio data is not int16"

            stream.write(audio_data)
    finally:
        if transmit:
            ptt_off()
