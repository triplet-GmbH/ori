from nicegui import ui
from backend import controller

if __name__ in {"__main__", "__mp_main__"}:
    ui.run(port=8023, reload=True)
