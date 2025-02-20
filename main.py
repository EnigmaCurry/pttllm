import click
import numpy as np
import sounddevice as sd
from piper.voice import PiperVoice
from .tts import get_model

import logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

@click.command()
@click.option('--callsign', required=True, help='The callsign the LLM should use.')
def main(callsign):
    log.info(f"Starting Piper-TTS with callsign: {callsign}")

    model_path = get_model("en_GB-alan-low")
    if not model_path:
        log.error("Failed to load the model.")
        return

    voice = PiperVoice.load(model_path)

    stream = sd.OutputStream(samplerate=voice.config.sample_rate, channels=1, dtype='int16')
    stream.start()

    print(f"{callsign} is ready. Enter text to synthesize (type 'exit' to quit):")
    while True:
        text = input("> ")
        if text.lower() == "exit":
            break

        full_text = f"{callsign} says: {text}"
        for audio_chunk in voice.synthesize_stream_raw(full_text):
            audio_data = np.frombuffer(audio_chunk, dtype=np.int16)
            stream.write(audio_data)

    stream.stop()
    stream.close()
    log.info("Piper-TTS has stopped.")

if __name__ == '__main__':
    main()
