import math
from datetime import datetime
from decimal import Decimal

from financial.input import (
    FinancialDataInput,
    FinancialStatisticsInput,
    NullFinancialDataInput,
    NullFinancialStatisticsInput,
)
from financial.model import FinancialData, db


class FinancialDataInputValidationService:
    def __init__(self, request_args):
        self.validation_errors = []
        self.financial_data = self.validate_and_parse_financial_data_input(request_args)

    def validate_and_parse_financial_data_input(
        self, request_args
    ) -> FinancialDataInput | NullFinancialDataInput:
        start_date = request_args.get("start_date", datetime.now().strftime("%Y-%m-%d"))
        end_date = request_args.get("end_date", datetime.now().strftime("%Y-%m-%d"))
        for field_name, date in (("start_date", start_date), ("end_date", end_date)):
            try:
                datetime.strptime(date, "%Y-%m-%d")
            except ValueError:
                self.validation_errors.append(f"{field_name} is not a valid date")
                return NullFinancialDataInput()

        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

        if start_date > end_date:
            self.validation_errors.append("start_date is after end_date")
            return NullFinancialDataInput()

        # use "IBM" as default symbol
        symbol = request_args.get("symbol", "IBM")
        if symbol not in ["IBM", "AAPL"]:
            self.validation_errors.append("symbol is not valid")
            return NullFinancialDataInput()

        limit = request_args.get("limit", "5")

        # Use 1 as default page. Page 1 is the first page.
        page = request_args.get("page", "1")
        for field_name, value in [("limit", limit), ("page", page)]:
            try:
                int(value)
            except ValueError:
                self.validation_errors.append(f"{field_name} is not a valid integer")
                return NullFinancialDataInput()

        return FinancialDataInput(
            start_date=start_date,
            end_date=end_date,
            symbol=symbol,
            limit=int(limit),
            page=int(page),
        )


class FinancialStatisticsInputValidationService:
    def __init__(self, request_args):
        self.validation_errors = []
        self.financial_statistics = self.validate_and_parse_financial_statistics_input(
            request_args
        )

    def validate_and_parse_financial_statistics_input(
        self, request_args
    ) -> FinancialStatisticsInput | NullFinancialStatisticsInput:
        # check if all required fields are present
        for required_field in ("start_date", "end_date", "symbol"):
            if required_field not in request_args:
                self.validation_errors.append(f"{required_field} is required")
                return NullFinancialStatisticsInput()

        start_date = request_args.get("start_date")
        end_date = request_args.get("end_date")
        for field_name, date in (("start_date", start_date), ("end_date", end_date)):
            try:
                datetime.strptime(date, "%Y-%m-%d")
            except ValueError:
                self.validation_errors.append(f"{field_name} is not a valid date")
                return NullFinancialStatisticsInput()

        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

        if start_date > end_date:
            self.validation_errors.append("start_date is after end_date")
            return NullFinancialStatisticsInput()

        symbol = request_args.get("symbol")
        # symbol only allows IBM and AAPL
        if symbol not in ("IBM", "AAPL"):
            self.validation_errors.append("symbol is not valid")
            return NullFinancialStatisticsInput()

        return FinancialStatisticsInput(
            start_date=start_date, end_date=end_date, symbol=symbol
        )


class GetFinancialDataService:
    """Service to get financial data from database"""

    def __init__(self, financial_data_input: FinancialDataInput):
        self.financial_data_input = financial_data_input
        self.financial_data_output = []
        self.pagination = {}

    def get_financial_data(self) -> None:
        financial_data = db.session.scalars(
            db.select(FinancialData)
            .where(
                FinancialData.symbol == self.financial_data_input.symbol,
                FinancialData.date >= self.financial_data_input.start_date,
                FinancialData.date <= self.financial_data_input.end_date,
            )
            .order_by(FinancialData.date)
        ).all()

        self.format_pagination(len(financial_data))
        self.format_financial_data(financial_data)

    def format_financial_data(self, financial_data: list[FinancialData]) -> None:
        start_index = (
            self.financial_data_input.page - 1
        ) * self.financial_data_input.limit
        end_index = start_index + self.financial_data_input.limit
        self.financial_data_output = [
            {
                "symbol": row.symbol,
                "date": row.date.strftime("%Y-%m-%d"),
                "open_price": row.open_price,
                "close_price": row.close_price,
                "volume": row.volume,
            }
            for row in financial_data[start_index : end_index + 1]
        ]

    def format_pagination(self, total_length: int) -> None:
        # page starts at 1
        self.pagination = {
            "total": total_length,
            "limit": self.financial_data_input.limit,
            "page": self.financial_data_input.page,
            "pages": math.ceil(total_length / self.financial_data_input.limit),
        }


class CalculateFinancialStatisticsService:
    """Service to get financial data from database and calculate financial statistics"""

    def __init__(self, financial_statistics_input: FinancialStatisticsInput):
        self.financial_statistics_input = financial_statistics_input
        self.financial_statistics_output = {}

    def calculate_financial_statistics(self) -> None:
        financial_data = db.session.scalars(
            db.select(FinancialData).where(
                FinancialData.symbol == self.financial_statistics_input.symbol,
                FinancialData.date >= self.financial_statistics_input.start_date,
                FinancialData.date <= self.financial_statistics_input.end_date,
            )
        ).all()

        self.format_financial_statistics(financial_data)

    def format_financial_statistics(self, financial_data: list[FinancialData]) -> None:
        self.financial_statistics_output = {
            "symbol": self.financial_statistics_input.symbol,
            "start_date": self.financial_statistics_input.start_date.strftime(
                "%Y-%m-%d"
            ),
            "end_date": self.financial_statistics_input.end_date.strftime("%Y-%m-%d"),
            "average_daily_open_price": str(
                self.calculate_average_daily_open_price(financial_data)
            ),
            "average_daily_close_price": str(
                self.calculate_average_daily_close_price(financial_data)
            ),
            "average_daily_volume": str(
                self.calculate_average_daily_volume(financial_data)
            ),
        }

    def calculate_average_daily_volume(
        self, financial_data: list[FinancialData]
    ) -> Decimal:
        """Calculate average daily volume. Round to nearest integer"""
        return round(sum(row.volume for row in financial_data) / len(financial_data))

    def calculate_average_daily_open_price(
        self, financial_data: list[FinancialData]
    ) -> Decimal:
        """Calculate average daily open price. Round to 2 decimal places"""
        return round(
            (sum(row.open_price for row in financial_data) / len(financial_data)), 2
        )

    def calculate_average_daily_close_price(
        self, financial_data: list[FinancialData]
    ) -> Decimal:
        """Calculate average daily close price. Round to 2 decimal places"""
        return round(
            (sum(row.close_price for row in financial_data) / len(financial_data)), 2
        )
