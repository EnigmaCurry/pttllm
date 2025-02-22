import click
import numpy as np
import sounddevice as sd
import os
from dotenv import load_dotenv
from piper.voice import PiperVoice
from .tts import get_model, get_voices
from .audio import generate_silence, say, get_interface, \
    list_interfaces, validate_device
from .llm import respond_to_query
from .text import get_multiline_input

import logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

SYSTEM_PROMPT_DEFAULT = "You are a helpful assistant"

def get_env_or_default(env_var, default):
    return os.getenv(env_var, default)

@click.group()
@click.option('--dotenv', type=click.Path(exists=True), help='Path to a .env file to load environment variables.')
def cli(dotenv):
    """Push-To-Talk Large-Language-Model CLI"""
    if dotenv:
        load_dotenv(dotenv)
        log.info(f"Loaded environment variables from {dotenv}")

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

    interface_input = get_interface(input)
    interface_output = get_interface(output)
    voice = PiperVoice.load(model_path)
    if interface_output['max_output_channels'] < 1:
        raise ValueError(f"Audio interface has no output channels: {interface_output}")
    log.info(f"Output device: {interface_output}")
    try:
        stream = sd.OutputStream(
            samplerate=interface_output['default_samplerate'],
            channels=1,
            dtype='int16', device=(interface_input['index'], interface_output['index']))
    except:
        log.error(interface_output)
        raise
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
    list_interfaces()

@cli.command()
def list_voices():
    """List all voice models."""
    for voice in get_voices():
        print(voice)

if __name__ == '__main__':
    cli()
