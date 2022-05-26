from selenium.webdriver.remote.webelement import WebElement

from kspscraper.dto.communication_models import ItemCard
from kspscraper.model import KaspiParser, WebDriverManager


def create_kaspi_parser():
    return KaspiParser()


def create_web_driver_manager(city_name: str, url: str):
    return WebDriverManager(city_name=city_name, url=url)


class Scrapper:
    """ Класс предоставляет общие методы для сбора данных с web страниц магазина Kaspi.kz.
    Для открытия динамических страниц, используется selenium.webdriver,
    за парсинг данных на страницах отвечает KaspiParser.

      :Args:
        - city - город.
        - url - ссылка страницы поиска товара.
    """

    def __init__(self, url, city):
        self.url, self.city = url, city
        self._parser = create_kaspi_parser()
        self._web_driver_manager = create_web_driver_manager(city_name=city, url=url)

    def get_products_data(self) -> list[ItemCard]:
        """ Основная функция обработки web страницы,
         возвращает список из ItemCard """

        products = []

        with self._web_driver_manager as kaspi_wm:
            items_cards: list[WebElement] = kaspi_wm.get_item_cards()

            for card in items_cards:
                data = ItemCard(
                    title=self._parser.get_title(card),
                    link=self._parser.get_link(card),
                    discon=self._parser.get_discounts(card),
                    price=self._parser.get_price(card)
                )
                products.append(data)
        return products
