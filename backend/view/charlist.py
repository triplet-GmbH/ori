from tkinter.font import names
from nicegui import ui

from .header import render as header
from ..model.char import CharList, Char
from ..model.pagination import Pagination


def _add_char():
    char = Char(name="New Character")
    Char.insert(char)

    ui.notify("Character added", type="positive")
    ui.run_javascript('setTimeout(() => window.location.reload(), 1000)')


def render(chars: CharList, pagination: Pagination):
    header("list of chars")

    with ui.row():
        for char in chars.items:
            with ui.card().classes("col-5").on(
                'click',
                lambda e, i=char.id: ui.navigate.to(f'char/{i}/')
            ):
                with ui.card_section():
                    ui.label(char.name).classes("text-h5 text-center")

                with ui.card_section():
                    with ui.grid(columns=2):
                        ui.label("class:")
                        ui.label(char.classname)
                        ui.label("level:")
                        ui.label(char.level)

    with ui.footer().classes("w-full bg-stone-800 flex"):
        with ui.row().classes("flex-1 justify-center"):
            with ui.row().classes("flex justify-center items-center gap-4"):
                ui.button("<", on_click=lambda e: ui.navigate.to(f'/?page={max(pagination.current - 1, 1)}'))
                ui.label(pagination.current).classes("text-xl mx-10")
                ui.button(">", on_click=lambda e: ui.navigate.to(f'/?page={min(pagination.current + 1, pagination.maximum)}'))
        ui.button("new character", on_click=_add_char).classes("item")
