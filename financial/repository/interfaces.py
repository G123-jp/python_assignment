from abc import abstractmethod

from financial.schemas.finance import FinancialData
from typing import List


class BaseFinancialRepository:
    @abstractmethod
    def add_financial_data(self, entries: List[FinancialData]):
        """
        Add financial data to repository
        Parameters:
            List (FinancialData): The list of the FinancialData
        Returns:
            List (FinancialData): The list of the FinancialData
        """

    @abstractmethod
    def get_financial_data(self, symbol: str, start_date: str, end_date: str, limit: str, page: str):
        """
        Get financial data from repository
        Parameters:
            symbol (str): The symbol of financial data
            start_date (str): The query start date
            end_date (str): The query end date
            limit (str): The page limit
            page (str): The page number

        Returns:
            List (FinancialData): The list of the FinancialData
            Page (Pagination): The pagination object
        """


class BaseStatisticsRepository:
    @abstractmethod
    def get_statistics_data(self, symbol: str, start_date: str, end_date: str):
        """
        Get statistics data from repository
        Parameters:
            symbol (str): The symbol of statistics data
            start_date (str): The query start date
            end_date (str): The query end date

        Returns:
            List (StaticsData): The list of the StaticsData
        """
