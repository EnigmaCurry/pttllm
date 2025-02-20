def get_multiline_input(prompt="> "):
    print("Enter your text (press Enter on an empty line to finish):")
    lines = []
    while True:
        line = input(prompt)
        if line == "":
            break
        lines.append(line)
    return "\n".join(lines)


def split_text(text, wpm=150, duration_minutes=5):
    """
    Splits text into chunks based on word count, aiming for a specified duration at a given WPM.
    """
    words_per_chunk = wpm * duration_minutes

    words = text.split()

    chunks = []
    for i in range(0, len(words), words_per_chunk):
        chunk = ' '.join(words[i:i + words_per_chunk])
        chunks.append(chunk)

    return chunks
