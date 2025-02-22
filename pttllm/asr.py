from . import torch_patch
import whisper
import sounddevice as sd
import numpy as np
import queue
import sys
from collections import deque
import scipy.signal

def resample_audio(audio_data, orig_sr, target_sr):
    """Resample audio to target sample rate."""
    if orig_sr == target_sr:
        return audio_data
    duration = audio_data.shape[0] / orig_sr
    target_length = int(duration * target_sr)
    resampled_audio = scipy.signal.resample(audio_data, target_length)
    return resampled_audio.astype(np.float32)

class ASR:
    def __init__(self, model_name="base", samplerate=16000, vox_threshold=0.007,
                 silence_duration=1.5, silence_grace=0.5, pre_buffer_duration=0.5):
        # Load Whisper model
        self.model = whisper.load_model(model_name)
        self.samplerate = samplerate
        self.vox_threshold = vox_threshold
        self.silence_duration = silence_duration
        self.silence_grace = silence_grace
        self.pre_buffer_duration = pre_buffer_duration

        # Audio queue
        self.q = queue.Queue(maxsize=50)

        # Smoothing
        self.smoothing_factor = 0.9
        self.smoothed_level = 0

        self.is_transmitting = False

    def callback(self, indata, frames, time_info, status):
        """Audio callback."""
        if status.input_overflow and not self.is_transmitting:
            print("ASR: Input overflow detected!", file=sys.stderr)
        try:
            self.q.put_nowait(indata.copy())
        except queue.Full:
            print("ASR: Audio queue is full, dropping frame.", file=sys.stderr)

    def rms(self, data):
        """Calculate RMS of audio data."""
        return np.sqrt(np.mean(np.square(data)))

    def listen_and_transcribe(self, device, on_transcription):
        """Start listening and transcribing. Calls on_transcription with the result."""
        print("ASR: Listening for speech...")

        # Use the device's native sample rate
        device_samplerate = device['default_samplerate']

        with sd.InputStream(device=device['index'],
                            samplerate=device_samplerate,
                            channels=1,
                            blocksize=4096,
                            latency="low",
                            callback=self.callback):
            self.is_transmitting = False
            silence_counter = 0
            audio_buffer = []
            pre_buffer = deque(maxlen=int(device_samplerate * self.pre_buffer_duration / 1024))

            try:
                while True:
                    data = self.q.get()
                    pre_buffer.append(data)

                    # Apply RMS smoothing
                    level = self.rms(data)
                    self.smoothed_level = (self.smoothing_factor * self.smoothed_level) + \
                                          ((1 - self.smoothing_factor) * level)

                    if self.smoothed_level > self.vox_threshold:
                        silence_counter = 0
                        if not self.is_transmitting:
                            print("ASR: Transmission detected, recording...")
                            self.is_transmitting = True
                            audio_buffer = list(pre_buffer)

                        audio_buffer.append(data)

                    elif self.is_transmitting:
                        silence_counter += len(data) / device_samplerate
                        audio_buffer.append(data)

                        if silence_counter > self.silence_duration + self.silence_grace:
                            print("ASR: Transmission ended, transcribing...")
                            self.is_transmitting = False

                            # Prepare audio for Whisper
                            raw_audio = np.concatenate(audio_buffer, axis=0).flatten()

                            # Resample to 16000 Hz
                            audio_data = resample_audio(raw_audio, device_samplerate, self.samplerate)

                            # Transcribe with Whisper
                            result = self.model.transcribe(audio_data, fp16=False)
                            transcription = result["text"]
                            print("ASR: Transcription:", transcription)

                            # Call the provided callback
                            on_transcription(transcription)

            except KeyboardInterrupt:
                print("ASR: Stopped listening.")
