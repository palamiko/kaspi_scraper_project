import logging
from typing import Union

from peewee import DatabaseError, ModelSelect

from db_worker.dto.communication_models import PriceHistory
from db_worker.dto.db_models import TablePriceHistory, database
from db_worker.dto.response import MessageError


class CRUDRecordPrice:

    @classmethod
    def create_record_price(cls, data: list[tuple]) -> Union[None, MessageError]:
        """ Создает запись истории цены, для товара

          :argument
            data - список строк-кортежей вида [('val1-1', 'val1-2'), ('val2-1', 'val2-2')],
                   в последовательности: id_item, price, date_create
                   пример: [(3, 45000, '2022-05-25 19:38:56.061000'), (..), (..) ]

          :return: Union[None, MessageError]

        """

        price_h = TablePriceHistory
        fields = [price_h.id_item, price_h.price, price_h.date_create]

        try:
            with database.atomic():
                price_h.insert_many(rows=data, fields=fields).execute()

        except DatabaseError as ex:

            logging.exception(f"Exception in fun: {cls.create_record_price.__qualname__}. Arg: {data}")
            return MessageError(exception=repr(ex), exception_type='DataBaseException')

    @classmethod
    def get_history_price_item(cls, id_item: int) -> Union[tuple[PriceHistory], MessageError]:
        """ Получает все данные об изменениях цены для данного id_item из таблицы price_history

          :argument
            id_item - id товара из таблицы tracked_items

          :return:
            Возвращает кортеж из полученных экземпляров PriceHistory. -> tuple[TablePriceHistory, TablePriceHistory, ...]
        """
        data = []

        query = TablePriceHistory.select().where(TablePriceHistory.id_item == id_item)
        try:
            for i in query:
                # data.append(PriceHistory.from_orm(i))
                data.append(PriceHistory(**i.__data__))
            return tuple(data)
        except DatabaseError as ex:
            logging.exception(f"Exception in fun: {cls.get_history_price_item.__qualname__}. Arg:id_item={id_item}")
            return MessageError(exception=repr(ex), exception_type='DataBaseException')

    @classmethod
    def my_test(cls):
        query = TablePriceHistory.select().execute()
        print(type(query))
        print(query.__dict__)
        for i in query:
            print(type(i))
        a = PriceHistory.construct()

