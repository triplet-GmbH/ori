from nicegui import ui

from .header import render as header
from ..model.char import CharList


def render(chars: CharList):
    header("list of chars")

    with ui.row():
        for char in chars.items:
            with ui.card().classes("col-5").on(
                'click',
                lambda e, i=char.identifier: ui.navigate.to(f'char/{i}/')
            ):
                with ui.card_section():
                    ui.label(char.name).classes("text-h5 text-center")

                with ui.card_section():
                    with ui.grid(columns=2):
                        ui.label("class:")
                        ui.label(char.classname)
                        ui.label("level:")
                        ui.label(char.level)
