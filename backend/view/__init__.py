from datetime import datetime
from typing import Any

from nicegui import app

from ..model.char import Char, Change, AttPath


def binding(obj: object, attr: str|int) -> dict[str, Any]:
    def setter(element):
        if isinstance(attr, int):
            obj[attr] = element.value
        else:
            setattr(obj, attr, element.value)
    return {
        "value": obj[attr] if isinstance(attr, int) else getattr(obj, attr),
        "on_change": setter
    }


def history_binding(char: Char, path: AttPath) -> dict[str, Any]:
    def on_change(element):

        change = Change(
            username=app.storage.user['username'],
            path=path,
            datetime=datetime.now(),
            from_value=_walk_path(char, path),
            to_value=element.value,
        )

        char.changes = [
            *char.changes[:-1],
            *change.fold(char.changes[-1] if char.changes else None)
        ]

        target = _walk_path(char, path[:-1])
        if isinstance(path[-1], str):
            setattr(target, path[-1], element.value)
        elif isinstance(path[-1], int):
            target[path[-1]] = element.value
        else:
            raise ValueError(f"bad path fragment: {path[-1]!r}")

    return {
        "value": _walk_path(char, path),
        "on_change": on_change,
    }


def _walk_path(obj: Any, path: AttPath) -> Any:
    for field in path:
        if isinstance(field, str):
            obj = getattr(obj, field)
        elif isinstance(field, int):
            obj = obj[field]
        else:
            raise ValueError(f"bad path fragment: {field!r}")
    return obj