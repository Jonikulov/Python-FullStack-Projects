from nicegui import ui, app

ui.markdown("## **Disappearing Text Writing App**")

if __name__ in {"__main__", "__mp_main__"}:
    ui.run(
        host="0.0.0.0",
        port=8080,
        show=True,
        show_welcome_message=False,
    )
