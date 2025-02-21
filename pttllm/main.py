import click
import numpy as np
import sounddevice as sd
import os
from piper.voice import PiperVoice
from .tts import get_model
from .audio import generate_silence, say, get_interface
from .llm import respond_to_query
from .text import get_multiline_input

import logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

SYSTEM_PROMPT_DEFAULT = "You are a helpful assistant"

def get_env_or_default(env_var, default):
    return os.getenv(env_var, default)

@click.group()
def cli():
    """Push-To-Talk Large-Language-Model CLI"""
    pass

@cli.command()
@click.option('--callsign', default=lambda: get_env_or_default('PTTLLM_CALLSIGN', None), required=True, help='The callsign the LLM should use.')
@click.option('--base-url', default=lambda: get_env_or_default('PTTLLM_BASE_URL', None), required=True, help='The LLM API base URL.')
@click.option('--api-key', default=lambda: get_env_or_default('PTTLLM_API_KEY', "api-key"), help='The LLM API key.')
@click.option('--model', default=lambda: get_env_or_default('PTTLLM_MODEL', ""), help='The LLM model name.')
@click.option('--prompt', default=lambda: get_env_or_default('PTTLLM_PROMPT', SYSTEM_PROMPT_DEFAULT), help='The LLM system prompt.')
@click.option('--chunk-transmission', default=lambda: get_env_or_default('PTTLLM_CHUNK_TRANSMISSION', 5), type=int, help='Transmit response in X minute chunks')
@click.option('--max-transmission', default=lambda: get_env_or_default('PTTLLM_MAX_TRANSMISSION', 10), type=int, help='Maximum transmission time in minutes.')
@click.option('--voice', default=lambda: get_env_or_default('PTTLLM_VOICE', "en_GB-alan-low"), help='The voice model')
@click.option('--input', default=lambda: get_env_or_default('PTTLLM_INPUT', "default"), help='The audio input interface name')
@click.option('--output', default=lambda: get_env_or_default('PTTLLM_OUTPUT', "default"), help='The audio output interface name')
def station(callsign, base_url, api_key, model, prompt,
            chunk_transmission, max_transmission, voice, input, output):
    if chunk_transmission > max_transmission:
        log.error("--chunk-transmission must be less than --max-transmission")
        exit(1)
    elif chunk_transmission >= 10:
        log.error("--chunk-transmission must be less than 10 minutes.")
        exit(1)

    log.info(f"--callsign: {callsign}")
    log.info(f"--base-url: {base_url}")
    log.info(f"--api-key: {api_key}")
    log.info(f"--model: {model}")
    log.info(f"--prompt: {prompt}")
    log.info(f"--chunk-transmission: {chunk_transmission}")
    log.info(f"--max-transmission: {max_transmission}")
    log.info(f"--voice: {voice}")
    log.info(f"--input: {input}")
    log.info(f"--output: {output}")

    model_path = get_model(voice)
    if not model_path:
        log.error("Failed to load the model.")
        return

    voice = PiperVoice.load(model_path)
    stream = sd.OutputStream(samplerate=voice.config.sample_rate, channels=1,
                             dtype='int16', device=(input, output))
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

@cli.command()
def list_devices():
    """List all audio devices."""
    devices = sd.query_devices()
    for idx, device in enumerate(devices):
        print(f"{idx}: {device['name']} - Input Channels: {device['max_input_channels']}, Output Channels: {device['max_output_channels']}")

if __name__ == '__main__':
    cli()
