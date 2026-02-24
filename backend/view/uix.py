from typing import Optional
import re

from nicegui import ui
from nicegui.element import Element
from nicegui.events import ValueChangeEventArguments, Handler

_pattern = re.compile(r"^(-?\d*)(.*)$")


def input(
    value: str = '',
    placeholder: Optional[str] = None,
    on_change: Optional[Handler[ValueChangeEventArguments]] = None,
) -> Element:
    def modifier(sign: int):
        def modify(e):
            match = _pattern.match(str(input.value))
            assert match, "regex should always match"
            count, text = match.groups()
            new_count = int(count or "0") + sign * int(diff_input.value)
            input.value = f"{new_count}{text}"
        return modify

    with ui.row() as row:
        input = ui.input(
                    value=value,
                    on_change=on_change,
                    placeholder=placeholder).classes("grow-1")

        with ui.button_group().classes("hidden") as group:
            ui.button(icon="add", on_click=modifier(1)).classes("p-1")
            diff_input = (ui.input(value="1")
                                .props("dense borderless input-class=text-center")
                                .classes("w-8 bg-primary"))
            ui.button(icon="remove", on_click=modifier(-1)).classes("p-1")

    row.on("focusin", js_handler=f'''evt => {{
        getHtmlElement({group.id}).classList.remove("hidden")
    }}''')

    row.on("focusout", js_handler=f'''evt => {{
        if (!getHtmlElement({row.id}).contains(evt.relatedTarget)) {{
            getHtmlElement({group.id}).classList.add("hidden")
        }}
    }}''')

    return row


__all__ = [
    "input",
]