from db_worker.dto.response import MessageError, Response
from db_worker.config import header


def prepare_answer(db_response, request_data, successful_code: int):

    if isinstance(db_response, MessageError):
        return Response(request_body=request_data, exception=db_response, code=500).json(), 500, header.APP_JSON
    else:
        return Response(request_body=request_data,
                        response_body=db_response,
                        code=successful_code).json(), successful_code, header.APP_JSON