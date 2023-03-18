from typing import List, Dict, Any

import falcon
from falcon import Request, Response


class EmptyRequestBodyValidator:

    def __call__(self, request: Request, response: Response, resource: object, params: Dict[str, Any]) -> None:
        if len(request.media) == 0:
            raise falcon.HTTPBadRequest(description='Request body cannot be empty')


class RequiredParametersValidator(EmptyRequestBodyValidator):

    def __init__(self, required_params_list: List[str]):
        self.required_params_list = required_params_list

    def __call__(self, request: Request, response: Response, resource: object, params: Dict[str, Any]) -> None:
        super().__call__(request, response, resource, params)
        missing_params = set(self.required_params_list) - set(request.media.keys())
        if len(missing_params) > 0:
            if len(missing_params) > 1:
                message = f'Parameters {[val for val in missing_params]} are required in request body'
            else:
                message = f'Parameter {missing_params.pop()} is required in request body'
            raise falcon.HTTPBadRequest(description=message)
