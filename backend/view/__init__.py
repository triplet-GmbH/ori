from typing import Any


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
