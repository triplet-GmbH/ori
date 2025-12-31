from nicegui import ui

from .header import render as header
from ..model.char import Char


def render(char: Char):
    header(f"detail of {char.name}")
