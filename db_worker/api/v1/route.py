from flask_pydantic import validate

from db_worker import app
from db_worker.config import header
from db_worker.crud.crud_record_price import CRUDRecordPrice
from db_worker.dto.query_models.query_parameters import QueryRecordPrice
from db_worker.dto.response import Response, MessageError


@app.get("/api/v1/history_price_item")
@validate()
def get_history_price_item(query: QueryRecordPrice):
    db_response = CRUDRecordPrice.get_history_price_item(id_item=query.item_id)
    if isinstance(db_response, MessageError):
        return Response(request_body=query.item_id, exception=db_response, code=402).json(), 402, header.APP_JSON
    else:
        return Response(body=db_response, code=201).json(), 201, header.APP_JSON


@app.post("/api/v1/create_record_price")
@validate()
def create_records_price(body: QueryRecordPrice):
    db_response = CRUDRecordPrice.create_record_price(data=body.data)

    if isinstance(db_response, MessageError):
        return Response(request_body=body.data, exception=db_response, code=402).json(), 402, header.APP_JSON
    else:
        return Response(request_body=body.data, code=201).json(), 201, header.APP_JSON
