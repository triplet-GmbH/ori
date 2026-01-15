from nicegui import ui

from .header import render as header
from ..model.char import Char


def render(char: Char):
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

    with ui.tabs().classes("w-full") as tabs:
        tab_attributes = ui.tab("Attributes & State")
        tab_skills = ui.tab("Skills & Spells")
        tab_inventory = ui.tab("Inventory")

    with ui.tab_panels(tabs, value=tab_attributes).classes("w-full"):
        with ui.tab_panel(tab_attributes).classes("w-full"):
            with ui.row().classes("w-full"):
                with ui.column().classes("flex-1 mr-10"):
                    ui.label("Attributes").classes("text-xl")        
                    with ui.grid(columns="auto 1fr").classes("w-full"):
                        for key, value in attributes:
                            ui.label(f"{value}:").classes("self-center font-medium w-full mr-3")
                            ui.input(value=getattr(char.attributes, key)).classes("w-full")

                with ui.column().classes("flex-1"):
                    ui.label("Hitpoints").classes("text-xl")
                    with ui.grid(columns="auto 1fr").classes("w-full"):
                        ui.label("Maximum:").classes("self-center font-medium w-full mr-3")
                        ui.label(char.attributes.constitution * char.level).classes("self-center font-medium w-full")
                        ui.label("Current:").classes("self-center font-medium w-full mr-3")
                        ui.input(value=0).classes("w-full")

                    ui.label("Manapoints").classes("text-xl")
                    with ui.grid(columns="auto 1fr").classes("w-full"):
                        ui.label("Maximum:").classes("self-center font-medium w-full mr-3")
                        ui.label(char.attributes.intelligence * char.level).classes("self-center font-medium w-full")
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

        with ui.tab_panel(tab_skills).classes("w-full"):
            ui.label("Skills").classes("text-xl")

            with ui.row().classes("w-full mb-6"):
                with ui.grid(columns="6fr 1fr 1fr 1fr 1fr 1fr").classes("w-full"):
                    for activity in char.skills:
                        ui.input(value=activity.name)
                        a1 = ui.select(dict([("", "")] + attributes), value=activity.power_attribute)
                        a2 = ui.select(dict([("", "")] + attributes), value=activity.control_attribute)
                        ui.label(f"{getattr(char.attributes, activity.power_attribute, 0)}").classes("self-center")
                        ui.label(f"{getattr(char.attributes, activity.control_attribute, 0)}").classes("self-center")
                        ui.input(value=activity.level)
                    
                    ui.input(value="", placeholder="[New Skill]")
                    ui.select(dict([("", "")] + attributes), value="")
                    ui.select(dict([("", "")] + attributes), value="")
                    ui.label("0").classes("self-center")
                    ui.label("0").classes("self-center")
                    ui.input(value=1)

            with ui.row().classes("w-full mb-6"):
                ui.label("Spells").classes("text-xl")

                with ui.grid(columns="6fr 1fr 1fr 1fr 1fr 1fr").classes("w-full"):
                    for activity in char.spells:
                        ui.input(value=activity.name)
                        a1 = ui.select(dict([("", "")] + attributes), value=activity.power_attribute)
                        a2 = ui.select(dict([("", "")] + attributes), value=activity.control_attribute)
                        ui.label(f"{getattr(char.attributes, activity.power_attribute, 0)}").classes("self-center")
                        ui.label(f"{getattr(char.attributes, activity.control_attribute, 0)}").classes("self-center")
                        ui.input(value=activity.level)
                    
                    ui.input(value="", placeholder="[New Spell]")
                    ui.select(dict([("", "")] + attributes), value="")
                    ui.select(dict([("", "")] + attributes), value="")
                    ui.label("0").classes("self-center")
                    ui.label("0").classes("self-center")
                    ui.input(value=1)

        with ui.tab_panel(tab_inventory).classes("w-full"):
            ui.label("Inventory").classes("text-xl")

            with ui.grid(columns="1fr 1fr").classes("w-full"):
                for item in char.inventory:
                    ui.input(value=item)
                ui.input(value="", placeholder="[New Item]")


    with ui.footer().classes("w-full flex justify-center items-center p-4 bg-stone-800 gap-4"):
        ui.button("save")
        ui.button("reset")
        ui.button("exit")