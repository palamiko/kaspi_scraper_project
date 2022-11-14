from uuid import UUID

from pydantic import BaseModel


class QueryRecordPrice(BaseModel):
    item_id: int


class QueryHistoryPrice(BaseModel):
    data: list[tuple]


class QueryCreateItem(BaseModel):
    id_request: int
    title: str
    url: str
    uuid: str


class QueryCreateItems(BaseModel):
    items_list: list[tuple]


class QueryIDRequest(BaseModel):
    id_request: int


class QueryCreateTrackRequest(BaseModel):
    name_tack: str
    uuid: UUID


class QueryNotTrackRequest(BaseModel):
    id_request: int
