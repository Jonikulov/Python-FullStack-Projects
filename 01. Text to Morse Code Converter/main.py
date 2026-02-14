MORSE_MAP = {
    "A": "·-",
    "B": "-···",
    "C": "-·-·",
    "D": "-··",
    "E": "·",
    "F": "··-·",
    "G": "--·",
    "H": "····",
    "I": "··",
    "J": "·---",
    "K": "-·-",
    "L": "·-··",
    "M": "--",
    "N": "-·",
    "O": "---",
    "P": "·--·",
    "Q": "--·-",
    "R": "·-·",
    "S": "···",
    "T": "-",
    "U": "··-",
    "V": "···-",
    "W": "·--",
    "X": "-··-",
    "Y": "-·--",
    "Z": "--··",
    "0": "-----",
    "1": "·----",
    "2": "··---",
    "3": "···--",
    "4": "····-",
    "5": "·····",
    "6": "-····",
    "7": "--···",
    "8": "---··",
    "9": "----·",
    ".": "·-·-·-",
    ",": "--··--",
    ":": "---···",
    ";": "-·-·-·",
    "?": "··--··",
    "'": "·----·",
    "-": "-····-",
    "_": "··--·-",
    "/": "-··-·",
    "(": "-·--·",
    ")": "-·--·-",
    '"': "·-··-·",
    "=": "-···-",
    "+": "·-·-·",
    "@": "·--·-·",
    "!": "-·-·--",
}

def text_to_morse(input_msg: str) -> str:
    morse_code = " ".join(MORSE_MAP.get(ch.upper(), "#") for ch in input_msg)
    return morse_code


def play_morse_audio(morse_code: str) -> None:
    print("*sounds*")


def main():
    message_text = input("Input Your Message: ")
    morse_code = text_to_morse(message_text)
    print("Your Morse Code:", morse_code)
    input("Press Enter to Listen Morse Audio...")
    print("Playing Morse Code as Audio: ...")
    play_morse_audio(morse_code)


if __name__ == "__main__":
    main()
