from abc import abstractmethod

from schemas import FinancialData
from typing import List, Union
from datetime import date


class BaseFinancialDataDB:
    @abstractmethod
    def add_financial_data(self, entries: List[FinancialData]):
        """Add financial data to repository"""

    @abstractmethod
    def get_financial_data(self, symbol: Union[str, None] = None,
                           start_date: Union[date, None] = None,
                           end_date: Union[date, None] = None):
        """Get financial data from repository"""
