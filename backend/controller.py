from nicegui import ui

from .view.charlist import render as render_charlist
from .view.chardetail import render as render_chardetail

from .model.char import CHARS, CharList


PAGE_SIZE = 8


@ui.page('/', dark=True)
def charlist(page: int = 0):
    render_charlist(
        CharList(
            items=CHARS.items[page*PAGE_SIZE:(page+1)*PAGE_SIZE]
        )
    )


@ui.page('/char/{identifier}/', dark=True)
def char_detail(identifier: int):
    for char in CHARS.items:
        if char.identifier == identifier:
            render_chardetail(char)
            return
