from nicegui import ui


def render(title: str):
    with ui.header():
        ui.label(f"ORI - {title}").classes("text-h4")
