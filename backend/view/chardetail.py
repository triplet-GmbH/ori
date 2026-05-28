from typing import Any, Callable
from pydantic import ValidationError
from nicegui import ui

from ..model.char import Char, Activity

from . import history_binding
from . import uix


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
            ui.input(**history_binding(char, ["name"])).classes("w-full")
            ui.label("Class:").classes("self-center font-medium w-full mr-3")
            ui.input(**history_binding(char, ["classname"])).classes("w-full")
            ui.label("Level:").classes("self-center font-medium w-full mr-3")
            ui.input(**history_binding(char, ["level"])).classes("w-full")


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
                        uix.input(**history_binding(char, ['attributes', key])).classes("w-full")

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
                        uix.input(**history_binding(char, ['current', name])).classes("w-full")

                ui.label("Buffs / Debuffs").classes("text-xl")
                with ui.grid(columns="auto 1fr").classes("w-full"):
                    for num in range(1, 5):
                        ui.label(f"{num}:").classes("self-center font-medium w-full mr-3")
                        uix.input(**history_binding(char, ['current', f"buff_{num}"])).classes("w-full")


def _panel_skills(panel: ui.tab, char: Char, attributes: tuple[str]):
    with ui.tab_panel(panel).classes("w-full"):
        for name, label in [
            ("skills", "Skills"),
            ("spells", "Spells"),
        ]:
            ui.label(label).classes("text-xl")
            with ui.row().classes("w-full mb-6"):
                with ui.grid(columns="6fr 1fr 1fr 1fr 1fr").classes("w-full"):
                    ui.label("Name")
                    ui.label("Att 1")
                    ui.label("Att 2")
                    ui.label("Skill")
                    ui.label("Wert")

                    for index, activity in enumerate(getattr(char, name)):
                        ui.input(placeholder="" if activity.name else "[New Skill]", **history_binding(char, [name, index, "name"]))

                        ui.select(dict([("", "")] + attributes), **history_binding(char, [name, index, "power_attribute"]))
                        ui.select(dict([("", "")] + attributes), **history_binding(char, [name, index, "control_attribute"]))
                        ui.input(**history_binding(char, [name, index, "level"]))
                        skillvalue = (
                            (getattr(char.attributes, activity.power_attribute, 0) +
                            getattr(char.attributes, activity.control_attribute, 0)) *
                            (activity.level + 1)
                        )
                        ui.label(skillvalue).classes("self-center")


def _panel_inventory(panel: ui.tab, char: Char):
    with ui.tab_panel(panel).classes("w-full"):
        ui.label("Inventory").classes("text-xl")

        with ui.grid(columns="1fr 1fr").classes("w-full"):
            for index in range(len(char.inventory)):
                uix.input(placeholder="" if char.inventory[index] else "[New Item]", **history_binding(char, ['inventory', index]))


def _panel_check(panel: ui.tab, char: Char):

        activities = {
            **{x.name: x for x in char.skills},
            **{x.name: x for x in char.spells},
        }

        with ui.tab_panel(panel).classes("w-full"):
            ui.label("Check").classes("text-xl")
            s = ui.select(
                dict(
                    [("", "")] +
                    [(x, x[:30]) for x in activities]
                ),
            )

            def create(lb, ub):
                def calculate(skillname: str):
                    if a := activities.get(skillname):
                        skillvalue = (
                            (getattr(char.attributes, a.power_attribute, 0) +
                            getattr(char.attributes, a.control_attribute, 0)) *
                            (a.level + 1)
                        )

                        left = int(skillvalue // lb + 1) if lb != 0 else 0
                        right = int(skillvalue // ub) if ub != 0 else "∞"

                        return f"{left} - {right}"
                    else:
                        return ""
                return calculate

            skillvalue = 123

            with ui.grid(columns="2fr 1fr 1fr 1fr 1fr 1fr 1fr").classes("w-full"):
                ui.label("level")
                ui.label("mw")
                ui.label("fail")
                ui.label("miss")
                ui.label("hit")
                ui.label("crit")
                ui.label("crush")

                ui.label("lol")
                #ui.label(f"0 - {skillvalue // 3}")
                ui.label("").bind_text_from(s, 'value', backward=create(0, 3))

                ui.label("1")
                ui.label("2")
                ui.label("3")
                ui.label("5")
                ui.label("10")

                ui.label("easy")
                ui.label("").bind_text_from(s, 'value', backward=create(3, 3 / 2))
                ui.label("1")
                ui.label("3")
                ui.label("6")
                ui.label("10")
                ui.label("15")

                ui.label("medium")
                ui.label("").bind_text_from(s, 'value', backward=create(3 / 2, 3 / 4))
                ui.label("1")
                ui.label("4")
                ui.label("9")
                ui.label("14")
                ui.label("18")

                ui.label("hard")
                ui.label("").bind_text_from(s, 'value', backward=create(3 / 4, 1 / 2))
                ui.label("1")
                ui.label("5")
                ui.label("12")
                ui.label("18")
                ui.label("20")

                ui.label("epic")
                ui.label("").bind_text_from(s, 'value', backward=create(1 / 2, 0))
                ui.label("1")
                ui.label("6")
                ui.label("15")
                ui.label("19")
                ui.label("20")



def _panel_history(panel: ui.tab, char: Char):
    with ui.tab_panel(panel).classes("w-full"):
        with ui.grid(columns="1fr 1fr 1fr 1fr 1fr").classes("w-full"):
            ui.label("User")
            ui.label("Time")
            ui.label("What")
            ui.label("From")
            ui.label("To")

            for item in char.changes:
                ui.label(item.username)
                ui.label(item.datetime.strftime("%Y-%m-%d %H:%M:%S"))
                ui.label('.'.join(str(fragment) for fragment in item.path))
                ui.label(str(item.from_value))
                ui.label(str(item.to_value))




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
        "Check",
        "History"
    ])
    #anchor = int(ui.run_javascript('return window.location.hash.substring(1);', ) or "0")
    with ui.tab_panels(tabs).classes("w-full"):
        _panel_attributes(panels[0], char, attributes)
        _panel_skills(panels[1], char, attributes)
        _panel_inventory(panels[2], char)
        _panel_check(panels[3], char)
        _panel_history(panels[4], char)

    hash_value = int(await ui.run_javascript('return window.location.hash.substring(1);') or "0")
    tabs.value = panels[hash_value]
