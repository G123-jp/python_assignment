from typing import Optional


class FalconServiceError(Exception):
    def __init__(self, message: Optional[str] = None):
        if not message:
            message = 'Falcon Service Error'
        super().__init__(message)


class ResourceNotFoundError(FalconServiceError):
    def __init__(self, message: Optional[str] = None):
        if not message:
            message = 'Resource Not Found Error'
        super().__init__(message)


class ApiClientError(Exception):
    def __init__(self, message: Optional[str] = None):
        if not message:
            message = 'Api Client Error'
        super().__init__(message)

