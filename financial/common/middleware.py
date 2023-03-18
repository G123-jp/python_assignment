from datetime import datetime

import falcon

from common.logging import LoggerMixin


class RequestValidation(LoggerMixin):
    def __init__(self):
        super(RequestValidation, self).__init__()
        self._excluded_resources = ('/liveness', '/readiness', '/version', '/')
        self._excluded_methods = {'OPTIONS'}

    @staticmethod
    def _check_mandatory_header_param(param: str, req: falcon.Request):
        param_value = req.get_header(param, required=True)
        req.context['headers'][param] = param_value

    @staticmethod
    def _check_optional_header_param(param: str, req: falcon.Request):
        param_value = req.get_header(param)
        if param_value:
            req.context['headers'][param] = param_value

    def process_request(self, req: falcon.Request, _: falcon.Response) -> None:
        """
        Process the request before routing it.
        """
        if req.path not in self._excluded_resources and req.method not in self._excluded_methods:
            req.context['headers'] = dict()

    @staticmethod
    def _add_to_header_params(param: str, req: falcon.Request, resp: falcon.Response):
        if param in req.context['headers']:
            resp.set_header(param, req.context['headers'][param])

    def process_response(self, req: falcon.Request, resp: falcon.Response, _, __: bool) -> None:
        if req.path not in self._excluded_resources and req.method not in self._excluded_methods:
            params = []
            for param in params:
                self._add_to_header_params(param, req, resp)


class Telemetry(LoggerMixin):
    def __init__(self):
        super(Telemetry, self).__init__()
        self._excluded_resources = ('/liveness', '/readiness', '/version', '/')
        self._excluded_methods = {'OPTIONS'}
        self._logging_header_params = ()

    def process_request(self, req: falcon.Request, _: falcon.Response) -> None:
        """
        Process the request before routing it.
        """
        if req.path not in self._excluded_resources and req.method not in self._excluded_methods:
            req.context['received_at'] = datetime.now()
            custom_data = dict()
            if req.params:
                custom_data.update(req.params)
            if req.media:
                custom_data.update(req.media)
            for header_param in self._logging_header_params:
                if header_param in req.context['headers']:
                    custom_data[header_param] = req.context['headers'][header_param]
            custom_data['path'] = req.path
            self._logger.bind(**custom_data).info("Request received", custom_data)

    def process_response(self, req: falcon.Request, resp: falcon.Response, _, __: bool) -> None:
        if req.path not in self._excluded_resources and req.method not in self._excluded_methods:
            if 'received_at' in req.context:
                duration = (datetime.now() - req.context['received_at']).total_seconds()
                custom_data = {"response_status": resp.status, "req_duration_seconds": duration}
                self._logger.bind(**custom_data).info(f"Request completed in {duration:.3f} seconds")
