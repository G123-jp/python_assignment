from datetime import datetime
from enum import Enum

class Helpers():
    @staticmethod
    def print_text(text, error=False):
        """
        Prints a colored text to the console.

        Args:
            text (str): The text to be printed.
            error (bool, optional): Whether the text is an error message or not.
                                    If set to True, the text will be printed in red.
                                    If set to False or not specified, the text will be printed in blue.
        """
        text = str(text)
        if error:
            print('\033[91m' + text + '\033[0m')
        else:
            print('\033[94m' + text + '\033[0m')

    @staticmethod
    def get_root_cause(ex: Exception) -> str:
        """
        Helper function to get the root cause of the exception
        """
        while ex.__cause__ is not None:
            ex = ex.__cause__
        return str(ex)

    @staticmethod
    def get_date(date_str):
        """
        Helper function to convert date string to date object
        """
        return datetime.strptime(date_str, '%Y-%m-%d').date()

class StockSymbol(Enum):
    Apple   = "AAPL"    # --> Ticker symbol for Apple Inc.
    IBM     = "IBM"     # --> Ticker symbol for IBM Corporation