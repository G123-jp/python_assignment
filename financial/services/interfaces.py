from abc import abstractmethod


class BaseFinancialService:
    @abstractmethod
    def get_financial_data(self, start_date, end_date, symbol, page, limit):
        """Get finance data for a given start, end date and symbol."""
