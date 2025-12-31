from typing import List
from pydantic import BaseModel


class Char(BaseModel):
    identifier: int
    name: str
    classname: str
    level: int


class CharList(BaseModel):
    items: List[Char]


CHARS = CharList(items=[
    Char(identifier=1, name="Arthas", classname="Paladin", level=80),
    Char(identifier=2, name="Jaina", classname="Mage", level=75),
    Char(identifier=3, name="Thrall", classname="Shaman", level=78),
    Char(identifier=4, name="Valeera", classname="Rogue", level=70),
    Char(identifier=5, name="Uther", classname="Paladin", level=85),
    Char(identifier=6, name="Illidan", classname="Demon Hunter", level=90),
    Char(identifier=7, name="Malfurion", classname="Druid", level=82),
    Char(identifier=8, name="Anduin", classname="Priest", level=65),
    Char(identifier=9, name="Garrosh", classname="Warrior", level=88),
    Char(identifier=10, name="Sylvanas", classname="Hunter", level=86),
])
