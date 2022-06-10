from typing import Union

from uuid import UUID

from pydantic import BaseModel


class TrackingRequest(BaseModel):
    id: Union[int, None]
    date_create: str
    date_end: str
    date_last_response: str
    name_track: str
    tracking: bool
    uuid: UUID

    class Config:
        orm_mode = True


class TrackedItems(BaseModel):
    date_create: str
    id: Union[int, None]
    id_request: int
    title: str
    url: str
    uuid: UUID

    class Config:
        orm_mode = True


class PriceHistory(BaseModel):
    date_create: str
    id: Union[int, None]
    id_item: int
    price: int

    class Config:
        orm_mode = True
