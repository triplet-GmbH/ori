from nicegui import ui
from fastapi import Request

from .view.charlist import render as render_charlist
from .view.chardetail import render as render_chardetail

from .model.char import Char, CharList
from .model.pagination import Pagination


PAGE_SIZE = 8


@ui.page('/', dark=True)
def charlist(page: int = 1):
    pagination = Pagination(
        current=page,
        maximum=(Char.count() - 1) // PAGE_SIZE + 1,
    )
    render_charlist(
        CharList.fetch_page(page - 1, PAGE_SIZE),
        pagination
    )


@ui.page('/char/{identifier}/', dark=True)
async def char_detail(identifier: str, request: Request):
    char = Char.fetch_by_id(identifier)

    if char:
        await render_chardetail(char)
    else:
        ui.notify(f"Character {identifier} not found")
