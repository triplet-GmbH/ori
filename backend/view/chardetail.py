from argparse import Action
from ast import Call
from typing import Any, Awaitable, Callable
from pydantic import ValidationError
from nicegui import ui

from ..model.char import Char, Activity
from . import binding


def _submit(char: Char):
    try:
        Char.update(char)
        ui.notify("Update succeded", type="positive")
        ui.run_javascript('setTimeout(() => window.location.reload(), 1000)')
    except ValidationError:
        ui.notify("Validation Error", type="negative")


def _delete(char: Char):
    char.deleted = True
    Char.update(char)
    ui.navigate.to("/")
    ui.notify("Character deleted", type="positive")


def _common(char: Char):
    with ui.row().classes("w-full mb-6"):
        ui.label("Common Info").classes("text-xl")
        with ui.grid(columns="auto 1fr").classes("w-full"):
            ui.label("Name:").classes("self-center font-medium w-full mr-3")
            ui.input(**binding(char, "name")).classes("w-full")
            ui.label("Class:").classes("self-center font-medium w-full mr-3")
            ui.input(**binding(char, "classname")).classes("w-full")
            ui.label("Level:").classes("self-center font-medium w-full mr-3")
            ui.input(**binding(char, "level")).classes("w-full")


def _tab_panel(panel_names: list[str]):
    panels = []
    with ui.tabs().classes("w-full") as tabs:
        for index, name in enumerate(panel_names):
            tab = ui.tab(name)
            tab.on("click", lambda e, index=index: ui.run_javascript(f"window.location.hash = '{index}';"))
            panels.append(
                tab
            )
    return tabs, panels


def _panel_attributes(panel: ui.tab, char: Char, attributes: tuple[str]):
    with ui.tab_panel(panel).classes("w-full"):
        with ui.row().classes("w-full"):
            with ui.column().classes("flex-1 mr-10"):
                ui.label("Attributes").classes("text-xl")
                with ui.grid(columns="auto 1fr").classes("w-full"):
                    for key, value in attributes:
                        ui.label(f"{value}:").classes("self-center font-medium w-full mr-3")
                        ui.input(**binding(char.attributes, key)).classes("w-full")

            with ui.column().classes("flex-1"):
                for name, label, maxvalue in [
                    ("hitpoints", "Hitpoints", char.attributes.constitution * char.level),
                    ("manapoints", "Manapoints", char.attributes.intelligence * char.level),
                ]:
                    ui.label(label).classes("text-xl")
                    with ui.grid(columns="auto 1fr").classes("w-full"):
                        ui.label("Maximum:").classes("self-center font-medium w-full mr-3")
                        ui.label(maxvalue).classes("self-center font-medium w-full")
                        ui.label("Current:").classes("self-center font-medium w-full mr-3")
                        ui.input(**binding(char.current, name)).classes("w-full")

                ui.label("Buffs / Debuffs").classes("text-xl")
                with ui.grid(columns="auto 1fr").classes("w-full"):
                    for num in range(1, 5):
                        ui.label(f"{num}:").classes("self-center font-medium w-full mr-3")
                        ui.input(**binding(char.current, f"buff_{num}")).classes("w-full")


def _panel_skills(panel: ui.tab, char: Char, attributes: tuple[str]):
    with ui.tab_panel(panel).classes("w-full"):
        for name, label in [
            ("skills", "Skills"),
            ("spells", "Spells"),
        ]:
            ui.label(label).classes("text-xl")
            with ui.row().classes("w-full mb-6"):
                with ui.grid(columns="6fr 1fr 1fr 1fr 1fr 1fr").classes("w-full"):
                    for activity in getattr(char, name):
                        ui.input(placeholder="" if activity.name else "[New Skill]", **binding(activity, "name"))
                        ui.select(dict([("", "")] + attributes), **binding(activity, "power_attribute"))
                        ui.select(dict([("", "")] + attributes), **binding(activity, "control_attribute"))
                        ui.label(f"{getattr(char.attributes, activity.power_attribute, 0)}").classes("self-center")
                        ui.label(f"{getattr(char.attributes, activity.control_attribute, 0)}").classes("self-center")
                        ui.input(**binding(activity, "level"))


def _panel_inventory(panel: ui.tab, char: Char):
        with ui.tab_panel(panel).classes("w-full"):
            ui.label("Inventory").classes("text-xl")

            with ui.grid(columns="1fr 1fr").classes("w-full"):
                for index in range(len(char.inventory)):
                    ui.input(placeholder="" if char.inventory[index] else "[New Item]", **binding(char.inventory, index))


def _confirm_dialog(label: str, verb: str):
    with ui.dialog() as dialog, ui.card():
        ui.label(label)
        with ui.row().classes("justify-end w-full"):
            ui.button(verb, on_click=lambda: dialog.submit(True), color="negative")
            ui.button('Cancel', on_click=lambda: dialog.submit(False))

    def confirmation(action: Callable[[], Any]):
        async def _handle_dialog() -> None:
            if await dialog:
                action()
        return _handle_dialog
    return confirmation


async def render(char: Char):
    attributes = [
        ("strength", "Strength"),
        ("agility", "Agility"),
        ("constitution", "Constitution"),
        ("perception", "Perception"),
        ("intelligence", "Intelligence"),
        ("willpower", "Willpower"),
        ("charisma", "Charisma"),
        ("luck", "Luck"),
    ]
    char.skills.append(Activity(name="", power_attribute="", control_attribute="", level=1))
    char.spells.append(Activity(name="", power_attribute="", control_attribute="", level=1))
    char.inventory.append("")

    confirm = _confirm_dialog("Are you sure you want to delete this character?", "Delete")

    with ui.header():
        with ui.row().classes("flex-1"):
            ui.button("save", on_click=lambda e, char=char: _submit(char), color="secondary")
            ui.button("exit", on_click=lambda : ui.navigate.to("/"))

        ui.button("delete character", on_click=confirm(lambda: _delete(char)), color="negative")

    _common(char)

    tabs, panels = _tab_panel([
        "Attributes & State",
        "Skills & Spells",
        "Inventory",
    ])
    #anchor = int(ui.run_javascript('return window.location.hash.substring(1);', ) or "0")
    with ui.tab_panels(tabs).classes("w-full"):
        _panel_attributes(panels[0], char, attributes)
        _panel_skills(panels[1], char, attributes)
        _panel_inventory(panels[2], char)

    hash_value = int(await ui.run_javascript('return window.location.hash.substring(1);') or "0")
    tabs.value = panels[hash_value]
