from kspscraper.scrapper_module import Scrapper

city = 'Рудный'
url = 'https://kaspi.kz/shop/search/?text=Samsung%20C32F391'


def main():
    scrapper = Scrapper(url=url, city=city)
    print(scrapper.get_products_data())


if __name__ == '__main__':
    main()
