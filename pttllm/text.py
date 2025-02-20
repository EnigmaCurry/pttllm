import re

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

def markdown_to_plaintext(markdown_text):
    """
    Converts Markdown text to plain text, stripping formatting that should not be spoken.
    """

    # Remove code blocks (triple backticks)
    text = re.sub(r'```.*?```', '', markdown_text, flags=re.DOTALL)

    # Remove inline code (single backticks)
    text = re.sub(r'`([^`]*)`', r'\1', text)

    # Remove images ![alt text](url)
    text = re.sub(r'!\[.*?\]\(.*?\)', '', text)

    # Remove links but keep the text [text](url)
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)

    # Remove bold (** or __)
    text = re.sub(r'(\*\*|__)(.*?)\1', r'\2', text)

    # Remove italics (* or _)
    text = re.sub(r'(\*|_)(.*?)\1', r'\2', text)

    # Remove strikethrough (~~)
    text = re.sub(r'~~(.*?)~~', r'\1', text)

    # Remove headers (lines starting with #)
    text = re.sub(r'^\s*#{1,6}\s*', '', text, flags=re.MULTILINE)

    # Remove blockquotes (> )
    text = re.sub(r'^\s*> ?', '', text, flags=re.MULTILINE)

    # Remove unordered list markers (-, *, +) and ordered lists (1., 2., etc.)
    text = re.sub(r'^\s*[-*+]\s+', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\s*\d+\.\s+', '', text, flags=re.MULTILINE)

    # Replace multiple newlines with a single newline
    text = re.sub(r'\n{2,}', '\n', text)

    # Strip leading/trailing whitespace
    return text.strip()
