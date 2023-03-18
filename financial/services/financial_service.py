from pyparsing import empty

from errors import DataNotFoundError
from repository import FinancialRepository
from schemas.responses import GetFinancialDataResponse, InfoResponse, FinancialData
from services import BaseFinancialService


class FinancialService(BaseFinancialService):
    def __init__(self, financial_repository: FinancialRepository):
        self._financial_repository = financial_repository

    def get_financial_data(self, start_date, end_date, symbol, limit, page):
        items, pagination = self._financial_repository.get_financial_data(start_date=start_date, end_date=end_date,
                                                                          symbol=symbol, limit=limit, page=page)
        if items:
            return GetFinancialDataResponse(data=[
                FinancialData(symbol=item.symbol, date=str(item.date), open_price=item.open_price, close_price=item.close_price,
                              volume=item.volume) for item in items], pagination=pagination, info=InfoResponse())
        else:
            raise DataNotFoundError(
                message=f'Data not found error in generating Financial Data')
