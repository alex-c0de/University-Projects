MORSE = {
    "a": ".-", "b": "-...", "c": "-.-.", "d": "-..", "e": ".", "f": "..-.",
    "g": "--.", "h": "....", "i": "..", "j": ".---", "k": "-.-", "l": ".-..",
    "m": "--", "n": "-.", "o": "---", "p": ".--.", "q": "--.-", "r": ".-.",
    "s": "...", "t": "-", "u": "..-", "v": "...-", "w": ".--", "x": "-..-",
    "y": "-.--", "z": "--..",
    "1": ".----", "2": "..---", "3": "...--", "4": "....-", "5": ".....",
    "6": "-....", "7": "--...", "8": "---..", "9": "----.", "0": "-----",
    " ": "/",
}

# Generate UNMORSE by using dictionary comprehension to swap the keys and values of MORSE.
UNMORSE = {x: y for (y, x) in zip(MORSE.keys(), MORSE.values())}


def encode_morse(s: str) -> str:
    latinString = s.lower()
    morseString = ""

    for c in latinString:
        morseString += MORSE.get(c, "?")
        morseString += " "

    return morseString.strip()


def decode_morse(s: str) -> str:
    morseSequence = s.split(" ")
    latinString = ""

    for block in morseSequence:
        latinString += UNMORSE.get(block, "?")

    return latinString
