from nicegui import ui
from nicegui.events import ValueChangeEventArguments

from core import text_to_morse, compose_morse_code_audio


def header():
    ui.markdown("## **Text2Morse**").classes("self-center")


def io_field():

    def handle_input(e: ValueChangeEventArguments) -> None:
        input_text = e.value
        output_area.value = text_to_morse(input_text)

    with ui.row().classes("mx-auto"):
        ui.textarea(
            label="Text (input)", on_change=handle_input
        ).classes("w-[35vw]")
        # ).props("clearable").classes("w-[35vw]")

        ui.separator().props("vertical")

        output_area = ui.textarea(
            label="Morse (output)"
        ).props("readonly").classes("w-[35vw] text-3xl")


def parameters():
    data = {"speed": 75, "frequency": 432, "volume": 50}
    with ui.card().classes("mx-auto w-[50vw] shadow-0"):
        with ui.list().props("dense").classes("w-full"):
            # --- Speed Row ---
            with ui.item():
                with ui.item_section().props("avatar"):
                    speed_label = ui.label(f"Speed: {data["speed"]}").classes("text-teal font-bold")
                with ui.item_section():
                    ui.slider(
                        min=1,
                        max=100,
                        value=data["speed"],
                        on_change=lambda e: speed_label.set_text(f"Speed: {e.value}")
                    ).props("label color=teal").classes("w-full")
            # --- Pitch (Frequency) Row ---
            with ui.item():
                with ui.item_section().props("avatar"):
                    frequency_label = ui.label(
                        f"Pitch: {data["frequency"]}"
                    ).classes("text-deep-orange font-bold")
                with ui.item_section():
                    ui.slider(
                        min=100,
                        max=1000,
                        value=data["frequency"],
                        on_change=lambda e: frequency_label.set_text(f"Pitch: {e.value}")
                    ).props("label color=deep-orange").classes("w-full")
            # --- Volume Row ---
            with ui.item():
                with ui.item_section().props("avatar"):
                    volume_label = ui.label(f"Volume: {data["volume"]}").classes("font-bold")
                with ui.item_section():
                    ui.slider(
                        min=1,
                        max=100,
                        value=data["volume"],
                        on_change=lambda e: volume_label.set_text(f"Volume: {e.value}")
                    ).props("label").classes("w-full")


def play_morse():
    # TODO: get `output_area` value / set this `morse_code` in io_field->handle_input
    morse_code = ".-- .--. -.-. -.-.- . -.- .-."
    morse_sound = compose_morse_code_audio(
        morse_code, speed=80, vol=50, freq=432, wave_type="sine",
    )
    a = ui.audio(morse_sound, controls=False)
    a.play()


def controllers():
    with ui.row().classes("mx-auto"):
        ui.button(text="Play", icon="play_circle", on_click=play_morse).props("outline")
            # ui.button(text="Pause", icon="pause").props("outline")
        ui.button(text="Stop", icon="stop").props("outline")
