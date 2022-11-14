from flask_pydantic import validate

from db_worker import app
from db_worker.api.v1.funs import prepare_answer
from db_worker.crud.crud_record_price import CRUDRecordPrice
from db_worker.crud.crud_tracked_items import CRUDTrackingItems
from db_worker.crud.crud_tracking_request import CRUDTrackingRequest
from db_worker.dto.query_models.query_parameters import *


@app.post("/api/v1/history_price/create_record")
@validate()
def create_records_price(body: QueryHistoryPrice):
    """ body: {"data": [[3, 42895, "2022-06-17 19:38:58.061000"], [3, 43988, "2022-06-21 19:38:58.061000"]]} """

    db_response = CRUDRecordPrice.create_record_price(data=body.data)
    return prepare_answer(db_response=db_response, request_data=body, successful_code=201)


@app.get("/api/v1/history_price/history_item")
@validate()
def get_history_price_item(query: QueryRecordPrice):
    """
      :param: ?item_id=22
    """

    db_response = CRUDRecordPrice.get_history_price_item(id_item=query.item_id)
    return prepare_answer(db_response=db_response, request_data=query, successful_code=200)


@app.post('/api/v1/items/create_item')
@validate()
def create_item(body: QueryCreateItem):
    """ body: {"id_request": 1, "title": "1", "url": "1", "uuid": "1"} """

    db_response = CRUDTrackingItems.create_item(
        id_request=body.id_request,
        title=body.title,
        url=body.url,
        uuid=body.uuid)
    return prepare_answer(db_response=db_response, request_data=body, successful_code=201)


@app.post('/api/v1/items/create_items')
@validate()
def create_items(body: QueryCreateItems):
    """
    :input json
    {"items_list":
    [
        ["2022-07-20 12:21:30.033", 2, "Nokia A54", "http://mail.ru", "415deb7d-9521-4f12-ad5e-feaafcb898bb"],
        ["2022-07-21 12:22:30.033", 2, "Nokia A53", "http://mail11.ru", "416deb7d-9521-4f12-ad5e-feaafcb898bb"]
    ]
    }
    """
    db_response = CRUDTrackingItems.create_items(body.items_list)
    return prepare_answer(db_response=db_response, request_data=body, successful_code=201)


@app.get('/api/v1/items/get_id')
@validate()
def id_items(query: QueryIDRequest):
    db_response = CRUDTrackingItems.get_id_items(query.id_request)
    return prepare_answer(db_response=db_response, request_data=query, successful_code=200)


@app.get('/api/v1/tracked_request/create')
@validate()
def create_tracking(query: QueryCreateTrackRequest):
    db_response = CRUDTrackingRequest.create_tracking_request(name_track=query.name_tack, uuid=query.uuid)
    return prepare_answer(db_response=db_response, request_data=query, successful_code=201)


@app.get('/api/v1/tracked_request/all_tracked_position')
@validate()
def get_all_tracked_position(query=None):
    db_response = CRUDTrackingRequest.get_tracked_positions()
    return prepare_answer(db_response=db_response, request_data=query, successful_code=200)


@app.get('/api/v1/tracked_request/not_track')
@validate()
def do_not_track(query: QueryNotTrackRequest):
    """
      :param
        ?id_request=8
    """

    db_response = CRUDTrackingRequest.set_do_not_track(query.id_request)
    return prepare_answer(db_response=db_response, request_data=query, successful_code=200)
