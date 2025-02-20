from .phonetic_alphabet import to_phonetic
from .audio import generate_silence, say
from .text import split_text, markdown_to_plaintext
from openai import OpenAI

import logging
log = logging.getLogger(__name__)
logging.getLogger("openai._base_client").setLevel(logging.DEBUG)

def query_llm(base_url, api_key, model, prompt, query):
    client = OpenAI(base_url=base_url, api_key=api_key)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": query}
        ],
        max_tokens=-1,
        temperature=0.7
    )
    return markdown_to_plaintext(response.choices[0].message.content.strip())

def respond_to_query(stream, voice, callsign="", query="",
                     chunk_transmission=5, max_transmission=10,
                     base_url="", api_key="api-key", model="",
                     prompt="You are a helpful assistant."):
    if not base_url:
        log.error("base_url is not defined")
        exit(1)

    phonetic_callsign = to_phonetic(callsign)

    # Initial response announcement
    say(stream, voice, f"This is {phonetic_callsign} automated station responding to LLM query")
    generate_silence(stream, voice, 0.5)

    # Query the LLM
    try:
        llm_response = query_llm(base_url=base_url, api_key=api_key, model=model, prompt=prompt, query=query)
    except Exception as e:
        say(stream, voice, f"Error querying LLM: {str(e)}")
        return

    # Split the response into chunks
    response_chunks = split_text(llm_response, duration_minutes=chunk_transmission)
    generate_silence(stream, voice, 1.0)

    # Calculate max allowed chunks based on max_transmission
    max_chunks = max_transmission // chunk_transmission
    truncated = len(response_chunks) > max_chunks

    # Iterate through allowed chunks and transmit
    for idx, chunk in enumerate(response_chunks[:max_chunks]):
        say(stream, voice, chunk)

        # If there are more chunks, announce continuation
        if idx < min(len(response_chunks), max_chunks) - 1:
            generate_silence(stream, voice, 0.5)
            say(stream, voice, f"{phonetic_callsign}, continuing response.")
            generate_silence(stream, voice, 0.5)

    # Final sign-off
    generate_silence(stream, voice, 0.5)
    if truncated:
        say(stream, voice, f"{phonetic_callsign}, truncating message. Clear and monitoring.")
    else:
        say(stream, voice, f"{phonetic_callsign}, clear and monitoring.")
