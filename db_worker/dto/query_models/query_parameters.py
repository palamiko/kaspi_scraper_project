from typing import Union

from pydantic import BaseModel


class QueryRecordPrice(BaseModel):
    item_id : Union[None, int]
    data: Union[None, list[tuple]]
