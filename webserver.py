from nicegui import ui
from backend import controller
from backend import config
from backend.model.migration import run_migrations


if __name__ in {"__main__", "__mp_main__"}:
    if config.RUN_MIGRATIONS:
        run_migrations()
    ui.run(port=8023, reload=config.AUTO_RELOAD, storage_secret=config.SESSION_SECRET)
