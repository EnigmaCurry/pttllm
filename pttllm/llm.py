from .phonetic_alphabet import to_phonetic
from .audio import generate_silence, say
from .text import split_text

def respond_to_query(stream, voice, callsign, query,
                     chunk_transmission=5, max_transmission=10):
    phonetic_callsign = to_phonetic(callsign)

    # Initial response announcement
    say(stream, voice, f"This is {phonetic_callsign} automated station responding to LLM query")
    generate_silence(stream, voice, 0.5)

    # Split the response into hard-coded 5-minute chunks
    response_chunks = split_text(query, duration_minutes=chunk_transmission)
    generate_silence(stream, voice, 1.0)

    # Calculate max allowed chunks based on max_transmission
    max_chunks = max_transmission // chunk_transmission  # Floor division to round down
    truncated = len(response_chunks) > max_chunks

    # Iterate through allowed chunks and transmit
    for idx, chunk in enumerate(response_chunks[:max_chunks]):
        say(stream, voice, chunk)

        # If there are more chunks, announce continuation
        if idx < max_chunks - 1:
            generate_silence(stream, voice, 0.5)
            say(stream, voice, f"{phonetic_callsign}, continuing response.")
            generate_silence(stream, voice, 0.5)

    # Final sign-off
    generate_silence(stream, voice, 0.5)
    if truncated:
        say(stream, voice, f"{phonetic_callsign}, truncating message. Clear and monitoring.")
    else:
        say(stream, voice, f"{phonetic_callsign}, clear and monitoring.")
