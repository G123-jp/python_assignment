from abc import abstractmethod


class BaseFinancialService:
    @abstractmethod
    def get_financial_data(self, start_date, end_date, symbol, page, limit):
        """Get finance data for a given start, end date and symbol."""


class BaseStatisticsService:
    @abstractmethod
    def get_statistics_data(self, start_date, end_date, symbol):
        """Get finance data for a given start, end date and symbol."""
