from pydantic import UUID7, BaseModel, ConfigDict


class CardGet(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID7
    title: str
    description: str | None = None
    rank: str
    version: int


class ColumnGet(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID7
    name: str
    rank: str
    cards: list[CardGet] = []


class BoardGet(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID7
    name: str
    columns: list[ColumnGet] = []
