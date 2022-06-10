import logging
from typing import Union

from uuid import UUID

from peewee import DatabaseError

from db_worker.config import get_datetime
from db_worker.dto.db_models import TableTrackingRequest
from db_worker.dto.response import MessageError


class CRUDTrackingRequest:

    @classmethod
    def create_tracking_request(cls, name_track: str, uuid: UUID) -> Union[TableTrackingRequest, MessageError]:
        """ Создает новую запись в таблице TrackingRequest.

        :argument
        name_track - поисковая строка
        uuid - uuid запроса

        :return:
          - Заполненный экземпляр TrackingRequest или сообщение об ошибке

        """

        try:
            return TableTrackingRequest.create(
                date_create=get_datetime(),
                name_track=name_track,
                tracking=True,
                uuid=uuid)
        except DatabaseError as ex:
            logging.exception(
                f"Exception in fun: {cls.create_tracking_request.__qualname__}"
                f" Arg: name_track={name_track}, uuid:{uuid}")
            return MessageError(exception=repr(ex), exception_type='DataBaseException')

    @classmethod
    def get_tracked_positions(cls) -> Union[list[dict], MessageError]:
        """ Возвращает список всех отслеживаемых позиций из таблицы TrackingRequest.

         :return:
           - Список словарей вида {id:x, date_last_response:y} или сообщение об ошибке
        """

        tracked_positions = []

        query = TableTrackingRequest \
            .select(TableTrackingRequest.id, TableTrackingRequest.date_last_response) \
            .where(TableTrackingRequest.tracking == True) \
            .dicts()

        try:
            for i in query.execute():
                tracked_positions.append(i)
            return tracked_positions
        except DatabaseError as ex:
            logging.exception(
                f"Exception in fun: {cls.get_tracked_positions.__qualname__}.")
            return MessageError(exception=repr(ex), exception_type='DataBaseException')

    @classmethod
    def set_do_not_track(cls, id_request: int):
        """ Помечает запрос как "Не отслеживаемый"

         :argument
           - id_request - id запроса в таблице tracking_request """

        try:
            TableTrackingRequest \
                .update(tracking=False, date_end=get_datetime()) \
                .where(TableTrackingRequest.id == id_request) \
                .execute()
        except DatabaseError as ex:
            logging.exception(
                f"Exception in fun: {cls.set_do_not_track.__qualname__}. Arg: id_request={id_request}")
            return MessageError(exception=repr(ex), exception_type='DataBaseException')
