from nicegui import ui

from .header import render as header
from ..model.char import Char, Activity


def _submit(charState: dict, char: Char):
    try:
        char.name = charState["name"].value
        char.classname = charState["classname"].value
        char.level = int(charState["level"].value)

        for name, item in charState["attributes"].items():
            setattr(char.attributes, name, int(item.value))

        for name, item in charState["current"].items():
            if name in ["hitpoints", "manapoints"]:
                func = int
            else:
                func = lambda v: v

            setattr(char.current, name, func(item.value))

        func = lambda k, v: int(v) if k == "level" else v
        for name in ["skills", "spells"]:
            setattr(char, name, [
                Activity(
                    **{k: func(k, v.value) for k, v in item.items() if not k.startswith("__")}
                ) for item in charState[name] if item["name"].value
            ])
        
        char.inventory = [
            item.value for item in charState["inventory"] if item.value
        ]
    except ValueError:
        ui.notify("Validation failed", type="negative")
        return

    updated = Char.update(char)
    if updated:
        ui.notify("Update succeded", type="positive")
        ui.run_javascript('setTimeout(() => window.location.reload(), 1000)')
    else:
        ui.notify("nothing to update", type="info")


def _common(charState: dict, char: Char):
    with ui.row().classes("w-full mb-6"):
        ui.label("Common Info").classes("text-xl")        
        with ui.grid(columns="auto 1fr").classes("w-full"):
            ui.label("Name:").classes("self-center font-medium w-full mr-3")
            charState["name"] = ui.input(value=char.name).classes("w-full")
            ui.label("Class:").classes("self-center font-medium w-full mr-3")
            charState["classname"] = ui.input(value=char.classname).classes("w-full")
            ui.label("Level:").classes("self-center font-medium w-full mr-3")
            charState["level"] = ui.input(value=char.level).classes("w-full")


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


def _panel_attributes(panel: ui.tab, charState: dict, char: Char, attributes: tuple[str]):
    with ui.tab_panel(panel).classes("w-full"):
        with ui.row().classes("w-full"):
            with ui.column().classes("flex-1 mr-10"):
                ui.label("Attributes").classes("text-xl")        
                with ui.grid(columns="auto 1fr").classes("w-full"):
                    for key, value in attributes:
                        ui.label(f"{value}:").classes("self-center font-medium w-full mr-3")
                        charState["attributes"][key] = ui.input(
                            value=getattr(char.attributes, key)
                        ).classes("w-full")

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
                        charState["current"][name] = ui.input(value=getattr(char.current, name)).classes("w-full")

                ui.label("Buffs / Debuffs").classes("text-xl")
                with ui.grid(columns="auto 1fr").classes("w-full"):
                    for num in range(1, 5):
                        ui.label(f"{num}:").classes("self-center font-medium w-full mr-3")
                        charState["current"][f"buff_{num}"] = ui.input(value=getattr(char.current, f"buff_{num}")).classes("w-full")


def _panel_skills(panel: ui.tab, charState: dict, char: Char, attributes: tuple[str]):
    with ui.tab_panel(panel).classes("w-full"):
        for name, label in [
            ("skills", "Skills"),
            ("spells", "Spells"),
        ]:
            ui.label(label).classes("text-xl")
            with ui.row().classes("w-full mb-6"):
                with ui.grid(columns="6fr 1fr 1fr 1fr 1fr 1fr").classes("w-full"):
                    for activity in getattr(char, name):
                        charState[name].append({
                            "name": ui.input(value=activity.name),
                            "power_attribute": ui.select(dict([("", "")] + attributes), value=activity.power_attribute),
                            "control_attribute": ui.select(dict([("", "")] + attributes), value=activity.control_attribute),
                            "__1": ui.label(f"{getattr(char.attributes, activity.power_attribute, 0)}").classes("self-center"),
                            "__2": ui.label(f"{getattr(char.attributes, activity.control_attribute, 0)}").classes("self-center"),
                            "level": ui.input(value=activity.level)
                        })
                    
                    charState[name].append({
                        "name": ui.input(value="", placeholder="[New Skill]"),
                        "power_attribute": ui.select(dict([("", "")] + attributes), value=""),
                        "control_attribute": ui.select(dict([("", "")] + attributes), value=""),
                        "__1": ui.label("0").classes("self-center"),
                        "__2": ui.label("0").classes("self-center"),
                        "level": ui.input(value=1),
                    })


def _panel_inventory(panel: ui.tab, charState: dict, char: Char):
        with ui.tab_panel(panel).classes("w-full"):
            ui.label("Inventory").classes("text-xl")

            with ui.grid(columns="1fr 1fr").classes("w-full"):
                for item in char.inventory:
                    charState["inventory"].append(
                        ui.input(value=item)
                    )

                charState["inventory"].append(
                    ui.input(value="", placeholder="[New Item]")
                )


async def render(char: Char):
    charState = {
        "attributes": {},
        "current": {},
        "skills": [],
        "spells": [],
        "inventory": [],
    }

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

    with ui.header():
        ui.button("save", on_click=lambda e, charState=charState, char=char: _submit(charState, char), color="secondary")
        ui.button("exit", on_click=lambda : ui.navigate.to("/"))

    _common(charState, char)

    tabs, panels = _tab_panel([
        "Attributes & State",
        "Skills & Spells",
        "Inventory",
    ])
    #anchor = int(ui.run_javascript('return window.location.hash.substring(1);', ) or "0")
    with ui.tab_panels(tabs).classes("w-full"):
        _panel_attributes(panels[0], charState, char, attributes)
        _panel_skills(panels[1], charState, char, attributes)
        _panel_inventory(panels[2], charState, char)

    hash_value = int(await ui.run_javascript('console.log("Hallo"); return window.location.hash.substring(1);') or "0")
    tabs.value = panels[hash_value]
