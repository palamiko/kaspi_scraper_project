from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class ScraperWebDriver:
    """ Базовый класс web драйвера, на базе движка gecko от Mozilla """

    def __init__(self, url, time_wait: int = 4):
        self.url = url
        self.time_wait = time_wait
        self.driver = webdriver.Firefox()


class ScraperWebDriverKaspi(ScraperWebDriver):
    """ Класс представляет собой web драйвер, адаптированный для работы
     с магазином Kaspi.kz """

    def __init__(self, city_name: str, url):
        super().__init__(url)
        self.city = city_name
        self.driver.wait = WebDriverWait(self.driver, self.time_wait)
        self._get_cards_page()

    def _get_cards_page(self):
        """ Получает страницу с карточками товаров, путем перехода
         по поисковой ссылке и выбора города в выпадающем окне"""

        self.driver.get(url=self.url)
        self.driver.wait.until(EC.presence_of_element_located((By.LINK_TEXT, self.city))).click()

    def get_item_cards(self) -> list[WebElement]:
        """ Возвращает список из карточек товаров взятых на странице в виде list[WebElement] """

        return self.driver.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'item-card')))


class WebDriverManager:
    """ Класс является контекстным менеджером для ScraperWebDriverKaspi
     и выполняет автоматическое закрытие web драйвера по завершении операций"""

    def __init__(self, city_name: str, url: str):
        self.__resource = ScraperWebDriverKaspi(city_name, url)

    def __enter__(self):
        return self.__resource

    def __exit__(self, type, value, traceback):
        self.__resource.driver.close()


class KaspiParser:
    """ Класс парсер страниц магазина Kaspi.kz

     Предоставляет методы:
     get_title - возвращает название товара в карточке
     get_link - возвращает ссылку на товар(карточку)
     get_discounts - возвращает в виде списка скидки и иные акции на товар(если есть)
     get_price - возвращает цену товара.
    """

    @staticmethod
    def get_title(card):
        title_element = card.find_element(By.CLASS_NAME, "item-card__name-link")
        return title_element.text

    @staticmethod
    def get_link(card):
        title_element: WebElement = card.find_element(By.CLASS_NAME, "item-card__name-link")
        link = title_element.get_attribute('href')
        return link

    @staticmethod
    def get_discounts(card) -> list[str]:
        links_image_bonus = []

        discounts: list[WebElement] = card.find_elements(By.CLASS_NAME, "bonus")
        for bonus in discounts:
            image = bonus.find_element(By.TAG_NAME, 'img')
            links_image_bonus.append(image.get_attribute('src'))
        return links_image_bonus

    @staticmethod
    def get_price(card) -> str:
        price_element: WebElement = card.find_element(By.CLASS_NAME, "item-card__prices-price")
        return price_element.text
