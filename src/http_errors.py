
class HTTPException(BaseException):
    status_code: int


class Error404(HTTPException):
    status_code = 404


class Error422(HTTPException):
    status_code = 422


class Error500(HTTPException):
    status_code = 500

