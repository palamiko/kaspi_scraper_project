from kspscraper.scrapper_module import Scrapper
import urllib.parse

city = 'Рудный'
url = 'https://kaspi.kz/shop/search/?text=Samsung%20Galaxy%20A13%204%20%D0%93%D0%91'  # Samsung Galaxy A13 4 ГБ


def main():
    a = urllib.parse.urlparse(url)
    print(a)
    print(urllib.parse.unquote(a.query))

    scrapper = Scrapper(url=url, city=city)
    print(scrapper.get_products_data())


if __name__ == '__main__':
    main()
