from nicegui import ui
from ..buildinfo import version


def render(title: str):
    with ui.header():
        ui.label(f"ORI - {title}").classes("text-h4")
        ui.label(f"{version}").classes("text-s self-center flex-1 text-right")
