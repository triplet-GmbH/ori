from typing import Optional
from nicegui import ui, app
from fastapi import Request
from fastapi.responses import RedirectResponse

from starlette.middleware.base import BaseHTTPMiddleware

from .view.charlist import render as render_charlist
from .view.chardetail import render as render_chardetail
from .view.login import render as render_login

from .model.char import Char, CharList
from .model.pagination import Pagination


PAGE_SIZE = 8


@app.add_middleware
class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        print("AuthMiddleware: dispatching request for", request.url.path)
        if not app.storage.user.get('authenticated', False):
            if (
                not request.url.path.startswith('/_nicegui')
                and request.url.path not in ['/login']
            ):
                return RedirectResponse(f'/login?redirect_to={request.url.path}')
        return await call_next(request)


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
async def char_detail(identifier: str):
    char = Char.fetch_by_id(identifier)

    if char:
        await render_chardetail(char)
    else:
        ui.notify(f"Character {identifier} not found")


@ui.page('/login')
def login(redirect_to: str = '/') -> Optional[RedirectResponse]:
    render_login(redirect_to)
