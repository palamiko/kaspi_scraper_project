from datetime import datetime
from typing import Union, Any

from pydantic import BaseModel
from pydantic.utils import GetterDict
from uuid import UUID

from db_worker.dto.db_models import TablePriceHistory


class PeeweeGetterDict(GetterDict):
    def get(self, key: Any, default: Any = None):
        res = getattr(self._obj, key, default)
        if isinstance(res, TablePriceHistory):
            return list(res)
        return res


class TrackingRequestSmall(BaseModel):
    id: int
    date_last_response: Union[None, datetime]


class TrackingRequestFull(TrackingRequestSmall):
    date_create: datetime
    date_end: Union[None, datetime]
    name_track: str
    tracking: bool
    uuid: UUID

    class Config:
        orm_mode = True


class TrackedItems(BaseModel):
    date_create: datetime
    id: Union[int, None]
    id_request: int
    title: str
    url: str
    uuid: UUID

    class Config:
        orm_mode = True


class PriceHistory(BaseModel):
    date_create: datetime
    id: Union[int, None]
    id_item: int
    price: int

    class Config:
        orm_mode = True
        # getter_dict = PeeweeGetterDict
