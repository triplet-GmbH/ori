from nicegui import ui

from .header import render as header
from ..model.char import Char


def render(char: Char):
    header(f"detail of {char.name}")
    with ui.row().classes("w-full mb-6"):
        ui.label("Common Info").classes("text-xl")        
        with ui.grid(columns="auto 1fr").classes("w-full"):
            ui.label("Name:").classes("self-center font-medium w-full mr-3")
            ui.input(value=char.name).classes("w-full")
            ui.label("Class:").classes("self-center font-medium w-full mr-3")
            ui.input(value=char.classname).classes("w-full")
            ui.label("Level:").classes("self-center font-medium w-full mr-3")
            ui.input(value=char.level).classes("w-full")

    with ui.row().classes("w-full gap-10 mb-6"):
        with ui.column().classes("flex-1"):
            ui.label("Attributes").classes("text-xl")        
            with ui.grid(columns="auto 1fr").classes("w-full"):
                for attribute, value in char.attributes.items():
                    ui.label(attribute).classes("self-center font-medium w-full mr-3")
                    ui.input(value=value).classes("w-full")

        with ui.column().classes("flex-1"):
            ui.label("Hitpoints").classes("text-xl")
            with ui.grid(columns="auto 1fr").classes("w-full"):
                ui.label("Maximum:").classes("self-center font-medium w-full mr-3")
                ui.label(char.attributes["constitution"] * char.level).classes("self-center font-medium w-full")
                ui.label("Current:").classes("self-center font-medium w-full mr-3")
                ui.input(value=0).classes("w-full")

            ui.label("Manapoints").classes("text-xl")
            with ui.grid(columns="auto 1fr").classes("w-full"):
                ui.label("Maximum:").classes("self-center font-medium w-full mr-3")
                ui.label(char.attributes["intelligence"] * char.level).classes("self-center font-medium w-full")
                ui.label("Current:").classes("self-center font-medium w-full mr-3")
                ui.input(value=0).classes("w-full")

            ui.label("Buffs / Debuffs").classes("text-xl")
            with ui.grid(columns="auto 1fr").classes("w-full"):
                ui.label("1st:").classes("self-center font-medium w-full mr-3")
                ui.input(value="").classes("w-full")
                ui.label("2nd:").classes("self-center font-medium w-full mr-3")
                ui.input(value="").classes("w-full")
                ui.label("3rd:").classes("self-center font-medium w-full mr-3")
                ui.input(value="").classes("w-full")
                ui.label("4th:").classes("self-center font-medium w-full mr-3")
                ui.input(value="").classes("w-full")

    with ui.row().classes("w-full mb-6"):
        ui.label("Skills").classes("text-xl")

        with ui.grid(columns="6fr 1fr 1fr 1fr 1fr").classes("w-full"):
            for index in range(10):
                ui.input(value="Nahkampf")
                a1 = ui.select(dict(zip(char.attributes.keys(), char.attributes.keys())))
                a2 = ui.select(dict(zip(char.attributes.keys(), char.attributes.keys())))
                ui.label(char.attributes.get(a1.value, 0) + char.attributes.get(a2.value, 0)).classes("self-center")
                ui.input(value="3")

    with ui.row().classes("w-full mb-6"):
        ui.label("Spells").classes("text-xl")

        with ui.grid(columns="6fr 1fr 1fr 1fr 1fr").classes("w-full"):
            for index in range(10):
                ui.input(value="Nahkampf")
                a1 = ui.select(dict(zip(char.attributes.keys(), char.attributes.keys())))
                a2 = ui.select(dict(zip(char.attributes.keys(), char.attributes.keys())))
                ui.label(char.attributes.get(a1.value, 0) + char.attributes.get(a2.value, 0)).classes("self-center")
                ui.input(value="3")

    with ui.row().classes("w-full"):
        ui.label("Inventory").classes("text-xl")

        with ui.grid(columns="1fr 1fr").classes("w-full"):
            for index in range(10):
                ui.input(value="Nahkampf")
                ui.input(value="Nahkampf")


    with ui.footer().classes("w-full flex justify-center items-center p-4 bg-stone-800 gap-4"):
        ui.button("save")
        ui.button("reset")
        ui.button("exit")