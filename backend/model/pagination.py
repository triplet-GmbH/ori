from pydantic import BaseModel


class Pagination(BaseModel):
    current: int
    maximum: int
