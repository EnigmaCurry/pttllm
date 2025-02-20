import click
import numpy as np
import sounddevice as sd
from piper.voice import PiperVoice
from .tts import get_model
from .audio import generate_silence, say
from .llm import respond_to_query
from .text import get_multiline_input

import logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

SYSTEM_PROMPT_DEFAULT = "You are a helpful assistant"

@click.command()
@click.option('--callsign', required=True, help='The callsign the LLM should use.')
@click.option('--base-url', required=True, help='The LLM API base URL.')
@click.option('--api-key', default="api-key", help='The LLM API key.')
@click.option('--model', default="", help='The LLM model name.')
@click.option('--prompt', default=SYSTEM_PROMPT_DEFAULT, help='The LLM system prompt.')
@click.option('--chunk-transmission', default=5, help='Transmit response in X minute chunks')
@click.option('--max-transmission', default=10, help='Maximum transmission time in minutes.', type=int)
def main(callsign, base_url, api_key, model, prompt, chunk_transmission, max_transmission):
    if chunk_transmission > max_transmission :
        log.error("--chunk-transmission must be less than --max-transmission")
        exit(1)
    elif chunk_transmission >= 10 :
        log.error("--chunk-transmission must be less than 10 minutes.")
        exit(1)

    log.info(f"--chunk-transmission: {chunk_transmission}")
    log.info(f"--max-transmission: {max_transmission}")
    log.info(f"--callsign: {callsign}")

    model_path = get_model("en_GB-alan-low")
    if not model_path:
        log.error("Failed to load the model.")
        return

    voice = PiperVoice.load(model_path)
    stream = sd.OutputStream(samplerate=voice.config.sample_rate, channels=1,
                             dtype='int16')
    stream.start()

    print(f"{callsign} is ready. Enter text to synthesize (type 'exit' to quit):")
    while True:
        query = get_multiline_input()
        if query.lower() == "exit":
            break
        respond_to_query(stream=stream, voice=voice,
                         callsign=callsign, query=query,
                         chunk_transmission=chunk_transmission,
                         max_transmission=max_transmission,
                         base_url=base_url, api_key=api_key, model=model)
    stream.stop()
    stream.close()
    log.info("Piper-TTS has stopped.")

if __name__ == '__main__':
    main()
