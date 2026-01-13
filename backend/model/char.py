from random import choice, randint
from typing import Optional

from pydantic import BaseModel, Field

from . import CurrentDB, PyObjectId


class Char(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    name: str
    classname: str
    level: int
    attributes: dict[str, int]

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
    def update(cls, char: "Char") -> "Char":
        return Char.from_mongo(
            CurrentDB.char.update_one(
                {"_id": char.id},
                char.to_mongo()
            )
        )


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
        attributes={k: randint(2, 6) + randint(2, 6) + randint(2, 6) for k in attributes}
    )
    return Char.insert(char)
