import datetime
from uuid import UUID

from peewee import DatabaseError

from db_worker.dto.db_models import TrackingRequest, TrackedItems, database, PriceHistory


def create_tracking_request(name_track: str, uuid: UUID) -> TrackingRequest:
    """ Создает новую запись в таблице TrackingRequest.

    :argument
    name_track - поисковая строка
    uuid - uuid запроса

    :return:
      - Заполненный экземпляр TrackingRequest """

    return TrackingRequest.create(
        date_create=get_datetime(),
        name_track=name_track,
        tracking=True,
        uuid=uuid)


def get_tracked_positions() -> list[dict]:
    """ Возвращает список отслеживаемых позиций из таблицы TrackingRequest.

     :return:
       - Список словарей вида {id:x, date_last_response:y} """

    tracked_positions = []
    query = TrackingRequest \
        .select(TrackingRequest.id, TrackingRequest.date_last_response) \
        .where(TrackingRequest.tracking == True) \
        .dicts()

    for i in query.execute():
        tracked_positions.append(i)
    return tracked_positions


def set_do_not_track(id_request: int):
    """ Помечает запрос как "Не отслеживаемый"

     :argument
       - id_request - id запроса в таблице tracking_request """

    try:
        TrackingRequest \
            .update(tracking=False, date_end=get_datetime()) \
            .where(TrackingRequest.id == id_request)
    except DatabaseError as ex:
        print(ex.orig)


def create_item(id_request: int, title: str, url: str, uuid: str):
    """ Создает одну запись о товаре в таблице tracking_request.

    :argument
      id_request - id запроса, внешний ключ из таблицы tracking_request
      title - название товара
      url - ссылка на товар
      uuid - uuid запроса

    :return:
      - Заполненный экземпляр TrackedItems """

    return TrackedItems.create(
        date_create=get_datetime(),
        id_request=id_request,
        title=title,
        url=url,
        uuid=uuid)


def create_items(data: list[tuple]):
    """ Создает массовую вставку данных с большим количеством товаров.
        Запрос выполняется одной транзакцией.

     :argument
       data - список строк-кортежей вида [('val1-1', 'val1-2'), ('val2-1', 'val2-2')],
              в последовательности: date_create, id_request, title, url, uuid
              пример: [('11.02.23', 8, 'Nokia A52', 'http://..', 'e23233-32fdv4ew-..'), (..), (..) ]
     """

    item = TrackedItems
    fields = [item.date_create, item.id_request, item.title, item.url, item.uuid]

    with database.atomic():
        item.insert_many(rows=data, fields=fields).execute()


def get_id_items(id_request) -> tuple:
    """ Получает id_items товаров из таблицы tracked_items

      :argument
        id_request - принимает id_request(внешний ключ) из таблицы tracking_request

      :return:
        Возвращает кортеж id_items отслеживаемых для данного id_request
    """

    data = []
    query = TrackedItems.select(TrackedItems.id).where(TrackedItems.id_request == id_request)
    for i in query:
        data.append(i.id)
    return tuple(data)


def get_price_history_item(id_item: int) -> tuple:
    """ Получает все данные об изменениях цены для данного id_item из таблицы price_history

      :argument
        id_item - id товара из таблицы tracked_items

      :return:
        Возвращает кортеж из полученных экземпляров PriceHistory. -> tuple[PriceHistory, PriceHistory, ... ]
    """
    data = []

    query = PriceHistory.select().where(PriceHistory.id_item == id_item)
    for i in query:
        data.append(i)
    return tuple(data)


def create_record_price(data: list[tuple]):
    """ Создает запись истории цены, для товара

      :argument
        data - список строк-кортежей вида [('val1-1', 'val1-2'), ('val2-1', 'val2-2')],
               в последовательности: id_item, price, date_create
               пример: [(3, 45000, '2022-05-25 19:38:56.061000'), (..), (..) ]

    """

    price_h = PriceHistory
    fields = [price_h.id_item, price_h.price, price_h.date_create]

    with database.atomic():
        price_h.insert_many(rows=data, fields=fields).execute()


def generate_list_tuples():
    """ data = [('val1-1', 'val1-2'),
        ('val2-1', 'val2-2'),
        ('val3-1', 'val3-2')] """
    data = []
    pass


def get_datetime():
    return datetime.datetime.now()
