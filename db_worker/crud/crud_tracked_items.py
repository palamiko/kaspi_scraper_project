import logging
from typing import Union
from uuid import UUID

from peewee import DatabaseError

from db_worker.config import get_datetime
from db_worker.dto.communication_models import TrackedItems
from db_worker.dto.db_models import TableTrackedItems, database
from db_worker.dto.response import MessageError


class CRUDTrackingItems:

    @classmethod
    def create_item(cls, id_request: int, title: str, url: str, uuid: str) -> Union[TrackedItems, MessageError]:
        """ Создает одну запись о товаре в таблице tracking_items.

        :argument
          id_request - id запроса, внешний ключ из таблицы tracking_request
          title - название товара
          url - ссылка на товар
          uuid - uuid запроса

        :return:
          - Заполненный экземпляр TableTrackedItems

        """

        try:
            response = TableTrackedItems.create(
                date_create=get_datetime(),
                id_request=id_request,
                title=title,
                url=url,
                uuid=uuid)
            return TrackedItems(**response.__data__)
        except DatabaseError as ex:
            logging.exception(
                f"Exception in fun: {cls.create_item.__qualname__}"
                f" Arg: id_request={id_request}, title={title}, url={url}, uuid={uuid}")
            return MessageError(exception=repr(ex), exception_type='DataBaseException')

    @classmethod
    def create_items(cls, data: list[tuple]) -> Union[None, MessageError]:
        """ Создает массовую вставку данных в таблице tracking_items с большим количеством товаров.
            Запрос выполняется одной транзакцией.

         :argument
           data - список строк-кортежей вида [('val1-1', 'val1-2'), ('val2-1', 'val2-2')],
                  в последовательности: date_create, id_request, title, url, uuid
                  пример: [('11.02.23', 8, 'Nokia A52', 'http://..', 'e23233-32fdv4ew-..'), (..), (..) ]
         """

        item = TableTrackedItems
        fields = [item.date_create, item.id_request, item.title, item.url, item.uuid]

        try:
            with database.atomic():
                item.insert_many(rows=data, fields=fields).execute()
        except DatabaseError as ex:
            logging.exception(
                f"Exception in fun: {cls.create_items.__qualname__} Arg: data={data}")
            return MessageError(exception=repr(ex), exception_type='DataBaseException')

    @classmethod
    def get_id_items(cls, id_request: int) -> Union[tuple, MessageError]:
        """ Возвращает id_items товаров из таблицы tracked_items

          :argument
            id_request - принимает id_request(внешний ключ) из таблицы tracking_request

          :return:
            Возвращает кортеж id_items отслеживаемых для данного id_request
        """

        data = []
        query = TableTrackedItems.select(TableTrackedItems.id).where(TableTrackedItems.id_request == id_request)
        try:
            for i in query:
                data.append(i.id)
            return tuple(data)
        except DatabaseError as ex:
            logging.exception(
                f"Exception in fun: {cls.get_id_items.__qualname__} Arg: data={data}")
            return MessageError(exception=repr(ex), exception_type='DataBaseException')