class FinancialDataInput:
    def __init__(self, start_date, end_date, symbol, limit, page):
        self.start_date = start_date
        self.end_date = end_date
        self.symbol = symbol
        self.limit = limit
        self.page = page


class NullFinancialDataInput:
    """This class is used to return a null object when the input is invalid."""
    start_date = None
    end_date = None
    symbol = ""
    limit = 0
    page = 0


class FinancialStatisticsInput:
    def __init__(self, start_date, end_date, symbol):
        self.start_date = start_date
        self.end_date = end_date
        self.symbol = symbol


class NullFinancialStatisticsInput:
    """This class is used to return a null object when the input is invalid."""
    start_date = None
    end_date = None
    symbol = ""
