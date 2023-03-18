from errors import DataNotFoundError
from financial.repository.mysql import StatisticsRepository
from schemas.responses import GetFinancialDataResponse, InfoResponse, FinancialData, GetStatisticsDataResponse
from schemas.statistics import StatisticsData
from financial.services.interfaces import BaseStatisticsService


class StatisticsService(BaseStatisticsService):
    def __init__(self, statistics_repository: StatisticsRepository):
        self._statistics_repository = statistics_repository

    def get_statistics_data(self, start_date, end_date, symbol):
        result = self._statistics_repository.get_statistics_data(start_date=start_date, end_date=end_date,
                                                                 symbol=symbol)
        if result is not None:
            return GetStatisticsDataResponse(
                data=StatisticsData(start_date=str(start_date), end_date=str(end_date), symbol=symbol,
                                    average_daily_open_price=round(float(result.average_daily_open_price), 2),
                                    average_daily_close_price=round(float(result.average_daily_close_price), 2),
                                    average_daily_volume=int(result.average_daily_volume)), info=InfoResponse())
        else:
            raise DataNotFoundError(
                message=f'Data not found error in generating Statistics Data')
