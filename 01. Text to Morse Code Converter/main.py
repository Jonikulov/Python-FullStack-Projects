import os
import uuid

from nicegui import ui
from nicegui.events import ValueChangeEventArguments, ClickEventArguments

from core import text_to_morse, compose_morse_code_audio

# =============== Configuration & Parameters ===============

LOGGING_CONFIG_1 = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "detailed": {
            "format": "[{asctime}.{msecs:03.0f} | {levelname} | {name} | {filename}:{lineno}]: {message}",
            "style": "{",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "detailed",
            "level": "WARNING",  # <--- Console only gets WARNING and ERROR
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "text2morse.log",
            "mode": "a",
            "maxBytes": 10**8,  # 100MB
            "backupCount": 5,   # 5 backups
            "encoding": "utf-8",
            "formatter": "detailed",
            "level": "INFO",    # <--- File gets INFO and everything above
        },
    },
    "loggers": {
        "": {  # Root logger (catches everything else)
            "handlers": ["console", "file"],
            "level": "INFO", 
        },
        "uvicorn": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False,
        },
        "uvicorn.access": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False,
        },
        "py.warnings": {  # Handles the captureWarnings(True) output
            "handlers": ["console", "file"],
            "level": "WARNING",
            "propagate": False,
        },
        "watchfiles.main": {  # Mutes the NiceGUI auto-reload spam
            "level": "WARNING",
            "propagate": False,
        }
    },
}

LOGGING_CONFIG_2 = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "detailed": {
            "format": "[{asctime}.{msecs:03.0f} | {levelname} | {name} | {filename}:{lineno}]: {message}",
            "style": "{",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "detailed",
            "level": "WARNING",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "text2morse.log",
            "mode": "a",
            "maxBytes": 10**8,  # 100MB
            "backupCount": 5,
            "encoding": "utf-8",
            "formatter": "detailed",
            "level": "INFO",
        },
    },
    "loggers": {
        "": {"handlers": ["console", "file"], "level": "INFO"},
        "watchfiles.main": {"level": "WARNING"},
        "uvicorn.access": {"propagate": True},
        "uvicorn.error": {"propagate": True},
    },
}

SOUND_TYPES = ["sine", "square", "sawtooth"]
ui.dark_mode(value=None)  # auto mode
default_params = {"speed": 75, "frequency": 432, "volume": 50}
morse_audio = None

# =============== Handlers & Controllers ===============

def handle_input(e: ValueChangeEventArguments) -> None:
    global output_area
    input_text = e.value
    output_area.value = text_to_morse(input_text)


def handle_finished():
    play_pause_button.set_text("Play")
    play_pause_button.set_icon("play_circle")


def set_volume(value: int):
    volume_label.set_text(f"Volume: {value}")
    if morse_audio is None:
        return
    # NiceGUI prefixes element IDs with a "c" in the actual HTML (e.g., c5).
    ui.run_javascript(f'document.getElementById("c{morse_audio.id}").volume={value/100}')


def control_morse_audio(e: ClickEventArguments) -> None:
    global morse_audio, output_area, speed_slider, pitch_slider, volume_slider

    morse_sound = compose_morse_code_audio(
        output_area.value,  # morse code
        speed=speed_slider.value,
        vol=100,
        freq=pitch_slider.value,
        wave_type=sound_type.value,
    )
    action = e.sender.text  # Play / Stop / Pause

    if action == "Play":
        e.sender.set_text("Pause")
        e.sender.set_icon("pause")
        if morse_audio is None:
            morse_audio = ui.audio(morse_sound, controls=False)
            morse_audio.on("ended", handle_finished)
        set_volume(volume_slider.value)
        morse_audio.play()
        stop_button.enable()
        return

    elif action == "Pause":
        e.sender.set_text("Play")
        e.sender.set_icon("play_circle")
        if morse_audio:
            morse_audio.pause()

    elif action == "Stop":
        if morse_audio is None:
            return
        morse_audio.pause()
        morse_audio.delete()
        # morse_audio.seek(0)  # Reset position to 0
        morse_audio = None
        stop_button.disable()
        play_pause_button.set_text("Play")
        play_pause_button.set_icon("play_circle")

# =============== User Interface ===============

ui.label("Text2Morse").classes("self-center text-4xl font-medium")

with ui.row().classes("mx-auto"):
    ui.textarea(label="Text (input)", on_change=handle_input) \
        .props("rows=17") \
        .classes("w-[40vw]  text-lg p-2 bg-[#fcf7f0] dark:bg-gray-600 rounded")
    ui.separator().props("vertical")
    output_area = ui.textarea(label="Morse (output)") \
        .props("readonly rows=17") \
        .classes("w-[40vw]  text-3xl bg-gray-100 p-2 dark:bg-[#3b3937] rounded")

with ui.card().classes("grid grid-cols-6 mx-auto w-[70vw] shadow-0"):
    with ui.column().classes("col-span-1 gap-0"):
        ui.label("Sound Type:").classes("text-bold")
        sound_type = ui.select(options=SOUND_TYPES, value="sine") \
        .classes("w-30")

    with ui.list().props("dense").classes("col-span-5 border-l"):
        # --- Speed Row ---
        with ui.item():
            with ui.item_section().props("avatar"):
                speed_label = ui.label(f"Speed: {default_params["speed"]}") \
                    .classes("text-teal font-bold")
            with ui.item_section():
                speed_slider = ui.slider(
                    min=1,
                    max=100,
                    value=default_params["speed"],
                    on_change=lambda e: speed_label.set_text(f"Speed: {e.value}")
                ).props("label color=teal").classes("w-full")
        # --- Pitch (Frequency) Row ---
        with ui.item():
            with ui.item_section().props("avatar"):
                frequency_label = ui.label(
                    f"Pitch: {default_params["frequency"]}"
                ).classes("text-deep-orange font-bold")
            with ui.item_section():
                pitch_slider = ui.slider(
                    min=100,
                    max=1000,
                    value=default_params["frequency"],
                    on_change=lambda e: frequency_label.set_text(f"Pitch: {e.value}")
                ).props("label color=deep-orange").classes("w-full")
        # --- Volume Row ---
        with ui.item():
            with ui.item_section().props("avatar"):
                volume_label = ui.label(f"Volume: {default_params["volume"]}") \
                    .classes("font-bold text-primary")
            with ui.item_section():
                volume_slider = ui.slider(
                    min=0,
                    max=100,
                    value=default_params["volume"],
                    on_change=lambda e: set_volume(e.value)
                ).props("label").classes("w-full")

with ui.row().classes("mx-auto"):
    play_pause_button = ui.button(
        text="Play", icon="play_circle", on_click=control_morse_audio
    ).props("outline no-caps")
    stop_button = ui.button(
        text="Stop", icon="stop", on_click=control_morse_audio
    ).props("outline no-caps")
    stop_button.disable()


if __name__ in {"__main__", "__mp_main__"}:
    ui.run(
        host="0.0.0.0",
        port=8081,
        reload=True,  # prod -> False
        show=True,  # prod -> False
        show_welcome_message=False,
        storage_secret=os.getenv("STORAGE_SECRET_KEY", uuid.uuid4()),
        # favicon="./static/images/logo-nobg.ico",
        title="Text to Morse Code Converter",
        uvicorn_logging_level="debug",  # prod -> info
        log_config=LOGGING_CONFIG_2,  # uvicorn logging configuration

        fastapi_docs=True,  # prod -> False
        workers=1,  # NiceGUI does not support multiple workers
    )
