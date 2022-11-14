from typing import Union, Any

from pydantic import BaseModel


class MessageError(BaseModel):
    exception: str
    exception_type: str


class Response(BaseModel):
    response_body: Union[Any, None]
    request_body: Union[Any, None]
    request_args: Union[Any, None]
    exception: Union[MessageError, None]
    fail: bool = False
    code: Union[int, None]

    def __init__(self, **data: Any):
        super().__init__(**data)

        if self.exception or self.code >= 300:
            self.fail = True
