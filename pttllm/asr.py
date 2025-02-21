from . import torch_patch
import whisper
import sounddevice as sd
import numpy as np
import queue
import sys
import time

# Load the Whisper model
model = whisper.load_model("base")

# Parameters
duration = 5  # seconds
samplerate = 16000  # Whisper uses 16kHz

# Setup queue for streaming audio
q = queue.Queue()

def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(indata.copy())

# Buffer to store audio data
audio_buffer = []

# Start recording
print("Recording...")
start_time = time.time()

with sd.InputStream(samplerate=samplerate, channels=1, callback=callback):
    while time.time() - start_time < duration:
        try:
            data = q.get(timeout=1)
            audio_buffer.append(data)
        except queue.Empty:
            print("Queue is empty, no audio data received.")
            break

print("Recording finished.")

# Convert list of arrays to a single NumPy array
if audio_buffer:
    audio_data = np.concatenate(audio_buffer, axis=0)
else:
    print("No audio data captured.")
    sys.exit(1)

# Whisper expects mono audio as float32
audio_data = audio_data.flatten().astype(np.float32)

# Transcribe the recorded audio
print("Transcribing...")
result = model.transcribe(audio_data, fp16=False)  # Set fp16=False if you're on CPU
print("Transcription:", result["text"])
