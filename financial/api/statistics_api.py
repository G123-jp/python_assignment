import falcon

from common.logging import LoggerMixin
from errors import DataNotFoundError
from errors.error_codes import StatisticsDataErrors
from services import StatisticsService


class StatisticsApi(LoggerMixin):
    def __init__(self, statistics_service: StatisticsService):
        self._statistics_service = statistics_service

    def on_get(self, req: falcon.Request, resp: falcon.Response):
        start_date = req.get_param('start_date')
        end_date = req.get_param('end_date')
        symbol = req.get_param('symbol')

        if start_date is not None and end_date is not None and symbol is not None:
            try:
                data = self._statistics_service.get_statistics_data(start_date=start_date, end_date=end_date,
                                                                    symbol=symbol)
                resp.body = data.to_json()
                resp.status = falcon.HTTP_200
            except DataNotFoundError as e:
                raise falcon.HTTPNotFound(description=str(e), code=StatisticsDataErrors.Statistics101.code,
                                          title=StatisticsDataErrors.Statistics101.title)
            except Exception as e:
                raise falcon.HTTPInternalServerError(description=str(e), code=StatisticsDataErrors.Statistics101.code,
                                                     title=StatisticsDataErrors.Statistics101.title)
        else:
            raise falcon.HTTPBadRequest(description='Required parameters are missing',
                                          code=StatisticsDataErrors.Statistics102.code,
                                          title=StatisticsDataErrors.Statistics102.title)
