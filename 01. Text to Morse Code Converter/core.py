import io
import wave
import base64

import numpy as np
from numpy.typing import NDArray

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
SAMPLE_RATE = 44100  # Standard CD quality

def text_to_morse(input_msg: str) -> str:
    morse_code = ""
    for ch in input_msg:
        morse_ch = MORSE_MAP.get(ch.upper())
        if morse_ch is not None:
            morse_code += morse_ch + " "
        elif ch.isspace():
            morse_code += ch
        else:
            morse_code += "# "
    return morse_code


def generate_beep_sound(
        freq: int = 432,
        duration: float = 1.0,
        vol: float = 0.5,
        wave_type: str | None = None,
    ) -> NDArray[np.int16]:
    # Calculate exactly how many "dots" we need for this duration
    num_samples = int(SAMPLE_RATE * duration)
    # The Time Array (The X-Axis)
    t = np.linspace(0, duration, num_samples, endpoint=False)
    # The "Shape" (values between -1.0 and 1.0)
    # Default 'sine'
    audio = np.sin(2 * np.pi * freq * t)
    if wave_type == "square":
        # "If sine is positive, be 1. Else -1."
        audio = np.sign(np.sin(2 * np.pi * freq * t))
    elif wave_type == "sawtooth":
        # The "% 1" creates the ramp: 0.1, 0.2 ... 0.9, 0.0, 0.1 ...
        ramp = (t * freq) % 1
        # Shift it to be between -1 and 1
        audio = (ramp * 2) - 1
    max_amplitude = 32767 * vol
    audio_int16 = (audio * max_amplitude).astype(np.int16)
    return audio_int16


def compose_morse_code_audio(
        morse_code: str,
        speed: int = 70,
        vol: int = 75,
        freq: int = 432,
        wave_type: str | None = None
    ) -> str:
    """Composes morse code (input) text to wav sound & returns as
    (bytes of) string"""
    # The In-Memory WAV File
    buffer = io.BytesIO()
    with wave.open(buffer, "wb") as wav_file:
    # with wave.open("out.wav", "wb") as wav_file:  # TODO: debug-temp
        wav_file.setnchannels(1)      # 1=mono
        wav_file.setsampwidth(2)      # 2 bytes = 16 bits
        wav_file.setframerate(SAMPLE_RATE)
        speed = 4 - (3.85 / 99) * (speed - 1)
        silence_count = 0
        for ch in morse_code:
            if ch == "-":
                duration = 0.25
                silence_count = 0
            elif ch == "·":
                duration = 0.1
                silence_count = 0
            # Limiting to add max 2 pauses in a row
            elif ch == " " and silence_count < 2:
                # Slightly longer silence/pause for separation of each word
                duration = 0.4
                silence_count += 1
            else:
                continue

            if duration != 0.4:
                # Add the morse code text sound byte
                beep_sound = generate_beep_sound(
                    freq=freq,
                    duration=duration * speed,
                    vol=vol / 100,
                    wave_type=wave_type
                )
                wav_file.writeframes(beep_sound.tobytes())
                # Add emptiness/silence to distinguish each character separately
                beep_sound = generate_beep_sound(duration=0.2 * speed, vol=0)
                wav_file.writeframes(beep_sound.tobytes())
            else:
                # Add emptiness/silence for separate each 'word'
                beep_sound = generate_beep_sound(
                    duration=duration * speed,
                    vol=0
                )
                wav_file.writeframes(beep_sound.tobytes())

    # Encdoe: Turn the binary WAV into a text string for the browser
    b64_audio = base64.b64encode(buffer.getvalue()).decode()
    print(b64_audio)
    return f"data:audio/wav;base64,{b64_audio}"


def main():
    message_text = input("Input Your Message: ")
    morse_code = text_to_morse(message_text)
    print("Your Morse Code:", morse_code)
    # input("Press Enter to Listen Morse Audio...")
    print("Playing Morse Code as Audio...")
    # TODO: user input parameters:
        # speed = [1 : 100]
        # vol = [1 : 100]
        # freq = [100 : 1_000]
    morse_sound = compose_morse_code_audio(
        morse_code, speed=80, vol=50, freq=432, wave_type="sine",
    )


if __name__ == "__main__":
    main()
