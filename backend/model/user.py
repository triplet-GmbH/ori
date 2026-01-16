from typing import Optional, Self

from pydantic import BaseModel, Field
from passlib.hash import pbkdf2_sha256 as password_hash

from . import CurrentDB, PyObjectId


class User(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")

    username: str
    password_hash: str

    # model_config = {
    #     "populate_by_name": True,
    #     "arbitrary_types_allowed": True
    # }

    def to_mongo(self):
        return self.model_dump(by_alias=True, exclude_none=True)

    @classmethod
    def from_mongo(cls, char: dict):
        return cls.model_validate(char)


    @classmethod
    def fetch_by_credentials(cls, username: str, password: str) -> Self | None:
        data = CurrentDB.user.find_one({"username": username})

        if not data or not password_hash.verify(password, data['password_hash']):
            return

        return cls.from_mongo(data)


    @classmethod
    def put(cls, username: str, password: str) -> None:
        CurrentDB.user.update_one(
            {'username': username},
            {"$set": {
                "password_hash": password_hash.hash(password)
            }},
            upsert=True
        )

