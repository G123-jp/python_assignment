import falcon

from common.logging import LoggerMixin
from errors import DataNotFoundError
from errors.error_codes import FinancialDataErrors
from services import FinancialService


class FinancialApi(LoggerMixin):
    def __init__(self, financial_service: FinancialService):
        self._financial_service = financial_service

    def on_get(self, req: falcon.Request, resp: falcon.Response):
        start_date = req.get_param('start_date')
        end_date = req.get_param('end_date')
        symbol = req.get_param('symbol')
        limit = req.get_param('limit')
        page = req.get_param('page')
        try:
            data = self._financial_service.get_financial_data(start_date=start_date, end_date=end_date, symbol=symbol,
                                                              limit=limit, page=page)
            resp.body = data.to_json()
            resp.status = falcon.HTTP_200
        except DataNotFoundError as e:
            raise falcon.HTTPNotFound(description=str(e), code=FinancialDataErrors.Financial101.code,
                                      title=FinancialDataErrors.Financial101.title)
        except Exception as e:
            raise falcon.HTTPInternalServerError(description=str(e), code=FinancialDataErrors.Financial101.code,
                                                 title=FinancialDataErrors.Financial101.title)
