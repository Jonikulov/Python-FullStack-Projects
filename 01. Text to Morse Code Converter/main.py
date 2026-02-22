import os
import uuid

from nicegui import ui, app

from user_interface import header, io_field, parameters, controllers

grid_style = (
    "border w-[60%] mx-auto p-[0.15rem] text-center text-lg text-bold "
    "gap-[0.15rem] shadow-xl/30 rounded dark:text-[#00ff41]"
)

@ui.page("/")
def index_page() -> None:
    # with ui.grid():
    header()
    io_field()
    parameters()
    controllers()


if __name__ in {"__main__", "__mp_main__"}:
    # app.on_startup(
    #     lambda: print("▶️ Live URLs:", app.urls)
    # )
    # TODO: setup proper parameters
    ui.run(
        host="0.0.0.0",
        port=8081,
        reload=True,  # prod -> False
        show=False,
        show_welcome_message=False,
        dark=True,

        storage_secret=os.getenv("STORAGE_SECRET_KEY", uuid.uuid4()),
        # favicon="./static/images/logo-nobg.ico",
        title="Text to Morse Code Converter",
        # TODO: make all logs & outputs to logfiles.
        uvicorn_logging_level="debug",  # prod -> info

        fastapi_docs=True,  # prod -> False
        workers=1,  # NiceGUI does not support multiple workers
    )

