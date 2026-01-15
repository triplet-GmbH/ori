from random import choice, randint
from typing import Optional

from pydantic import BaseModel, Field

from . import CurrentDB, PyObjectId


class Attributes(BaseModel):
    strength: int = 0
    agility: int = 0
    constitution: int = 0
    perception: int = 0
    intelligence: int = 0
    willpower: int = 0
    charisma: int = 0
    luck: int = 0


class Current(BaseModel):
    hitpoints: int = 0
    manapoints: int = 0
    buff_1: str = ""
    buff_2: str = ""
    buff_3: str = ""
    buff_4: str = ""


class Activity(BaseModel):
    name: str = ""
    power_attribute: str = ""
    control_attribute: str = ""
    level: int = 0


class Char(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    name: str
    classname: str = ""
    titles: str = ""

    level: int = 1

    attributes: Attributes = Attributes()
    current: Current = Current()

    skills: list[Activity] = []
    spells: list[Activity] = []
    inventory: list[str] = []

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True
    }

    def to_mongo(self):
        return self.model_dump(by_alias=True, exclude_none=True)

    @classmethod
    def from_mongo(cls, char: dict):
        return cls.model_validate(char)

    @classmethod
    def count(cls):
        return CurrentDB.char.count_documents({})

    @classmethod
    def fetch_by_id(cls, id: str) -> "Char":
        char = CurrentDB.char.find_one({
            "_id": PyObjectId(id)
        })
        if not char:
            return None
        
        return Char.from_mongo(char)

    @classmethod
    def insert(cls, char: "Char") -> "Char":
        result = CurrentDB.char.insert_one(
            char.to_mongo()
        )
        return Char.fetch_by_id(result.inserted_id)


    @classmethod
    def update(cls, char: "Char") -> bool:
        result = CurrentDB.char.replace_one(
            {"_id": char.id},
            char.to_mongo()
        )
        return result.modified_count == 1


class CharList(BaseModel):
    items: list[Char]

    @classmethod
    def fetch_page(cls, page: int, page_size: int) -> "CharList":
        return CharList(
            items=[
                Char.from_mongo(char)
                for char in CurrentDB.char.find()
                                          .skip(page * page_size)
                                          .limit(page_size)
            ]
        )
 

def generate_char() -> Char:
    attributes = [
        "strength", "agility", "constitution", "perception", "intelligence", "willpower", "charisma", "luck"
    ]
    names = [
        "Arthas", "Jaina", "Thrall", "Valeera", "Uther", "Illidan", "Malfurion", "Anduin", "Garrosh", "Sylvanas",
    ]
    classnames = ["Paladin", "Mage", "Shaman", "Rogue", "Druid", "Priest", "Warlock"]
    char = Char(
        name=f"{choice(names)} {choice(names)} {choice(names)}",
        classname=choice(classnames),
        level=randint(1, 100),
        attributes=Attributes(
            **{k: randint(2, 6) + randint(2, 6) + randint(2, 6) for k in attributes}
        )
    )
    char.current = Current(
        hitpoints=char.attributes.constitution * char.level,
        manapoints=char.attributes.intelligence * char.level,
    )

    return Char.insert(char)
