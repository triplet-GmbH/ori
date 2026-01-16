from nicegui import ui, app
from ..model.user import User

from .header import render as header


def render(redirect_to: str) -> None:
    header("Login")

    def try_login() -> None:
        user = User.fetch_by_credentials(username.value, password.value)
        if user:
            app.storage.user.update({
                'username': user.username,
                'authenticated': True
            })
            ui.notify('Login successful', color='positive')
            ui.navigate.to(redirect_to)
        else:
            ui.notify('Wrong username or password', color='negative')

    with ui.card().classes('absolute-center'):
        username = ui.input('Username').on('keydown.enter', try_login)
        password = ui.input('Password', password=True, password_toggle_button=True).on('keydown.enter', try_login)
        ui.button('Log in', on_click=try_login)
