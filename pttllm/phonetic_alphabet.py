ITU_PHONETIC_ALPHABET = {
    'A': 'Alpha',    'B': 'Bravo',     'C': 'Charlie',
    'D': 'Delta',    'E': 'Echo',      'F': 'Foxtrot',
    'G': 'Golf',     'H': 'Hotel',     'I': 'India',
    'J': 'Juliett',  'K': 'Kilo',      'L': 'Lima',
    'M': 'Mike',     'N': 'November',  'O': 'Oscar',
    'P': 'Papa',     'Q': 'Quebec',    'R': 'Romeo',
    'S': 'Sierra',   'T': 'Tango',     'U': 'Uniform',
    'V': 'Victor',   'W': 'Whiskey',   'X': 'X-ray',
    'Y': 'Yankee',   'Z': 'Zulu',
    '0': 'Zero',     '1': 'One',       '2': 'Two',
    '3': 'Three',    '4': 'Four',      '5': 'Five',
    '6': 'Six',      '7': 'Seven',     '8': 'Eight',
    '9': 'Nine'
}

def to_phonetic(text):
    """
    Translates the input text to its ITU phonetic alphabet equivalent.
    """
    phonetic_spelling = []

    for char in text.upper():
        if char in ITU_PHONETIC_ALPHABET:
            phonetic_spelling.append(ITU_PHONETIC_ALPHABET[char])
        elif char == ' ':
            phonetic_spelling.append(' ')  # Preserve spaces
        else:
            phonetic_spelling.append(f"[{char}]")  # Indicate unsupported characters

    return ' '.join(phonetic_spelling)
