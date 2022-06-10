import uuid
from uuid import UUID

from pydantic import BaseModel, HttpUrl


class BaseCommunionClass(BaseModel):
    uuid: UUID = uuid.uuid4()


class ItemCard(BaseCommunionClass):
    """ Определяет карточку товара.

      :arg:
        title - название товара
        link - ссылка на товар
        discon - ссылки на значки бонусов и скидок
        price - цена
    """

    title: str
    link: HttpUrl
    discon: list[str]
    price: str


