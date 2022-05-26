from dataclasses import dataclass
import uuid


@dataclass
class BaseCommunionClass(object):
    uuid = uuid.uuid4


@dataclass
class ItemCard(BaseCommunionClass):
    """ Определяет карточку товара.

      :arg:
        title - название товара
        link - ссылка на товар
        discon - ссылки на значки бонусов и скидок
        price - цена
    """

    title: str
    link: str
    discon: list[str]
    price: str

