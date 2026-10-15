
from pydantic import UUID7, BaseModel


class CardGet(BaseModel):
    id: UUID7
    title: str
    description: str | None = None
    rank: str
    version: int

class ColumnGet(BaseModel):
    id: UUID7
    name: str
    rank: str
    cards: list[CardGet] = []

class BoardGet(BaseModel):
    id: UUID7
    name: str
    columns: list[ColumnGet] = []


