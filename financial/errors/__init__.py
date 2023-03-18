from typing import Optional


class FalconServiceError(Exception):
    def __init__(self, message: Optional[str] = None):
        if not message:
            message = 'Falcon Service Error'
        super().__init__(message)


class DataNotFoundError(FalconServiceError):
    def __init__(self, message: Optional[str] = None):
        if not message:
            message = 'Data Not Found Error'
        super().__init__(message)


class ApiClientError(Exception):
    def __init__(self, message: Optional[str] = None):
        if not message:
            message = 'Api Client Error'
        super().__init__(message)


class DataBaseError(Exception):
    def __init__(self, message: Optional[str] = None):
        if not message:
            message = 'Database Error'
        super().__init__(message)

