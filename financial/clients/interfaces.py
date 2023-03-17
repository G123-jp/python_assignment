from abc import abstractmethod, ABC


class FinanceApiClient(ABC):
    """
    FinancialApiClient GET raw finance data and process for a given format.
    """

    @abstractmethod
    def get_raw_data(self, symbol):
        """
        Parameters:
            symbol (str): The symbol of the stock
        Returns:
            List of stock data
        """
        raise NotImplementedError

    @abstractmethod
    def process_raw_data(self, symbol, raw_data, duration):
        """
        Parameters:
            symbol (str): The symbol of the stock
            raw_data (list) : List of raw stock data
            duration : Time duration to process data
        Returns:
            List of FinancialData
        """
        raise NotImplementedError
