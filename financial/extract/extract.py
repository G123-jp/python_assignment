""" Model class for Extracted Data"""
from __future__ import annotations

from typing import Any, Dict, List

from dateutil import parser
from pydantic import BaseModel

from financial.constants import SYMBOLS, TimeFunctions, TimeFunctionsMap
from financial.extract.api_wrapper import get_core_stocks
from financial.helpers import sanetize_dict


class MetaData(BaseModel):
    Information: str
    Symbol: str
    LastRefreshed: str
    TimeZone: str


class TimeSeriesData(BaseModel):
    datetime: str
    open: str
    high: str
    low: str
    close: str
    volume: str

    @property
    def timestamp(self):
        return parser.parse(self.datetime)


class RawStock(BaseModel):
    MetaData: MetaData
    TimeSeries: List[TimeSeriesData]

    def __init__(__pydantic_self__, **data: Any) -> None:
        stock_data = RawStock.adjust_time_function_data(sanetize_dict(data))
        super().__init__(**stock_data)

    @staticmethod
    def adjust_time_function_data(stock_data) -> Dict[str, Any]:
        weekly_data: List[Dict[str, str]] = []
        for time, value in stock_data[
            TimeFunctionsMap[TimeFunctions.TIME_SERIES_WEEKLY]
        ].items():
            value["datetime"] = time
            weekly_data.append(value)
        stock_data["TimeSeries"] = weekly_data
        return stock_data


async def extract_stock() -> Dict[str, RawStock]:
    """Extracts Stocks"""
    extracted_data = sanetize_dict(
        await get_core_stocks(
            symbols=SYMBOLS,
            time_function=TimeFunctions.TIME_SERIES_WEEKLY.value,
        ),
    )
    return {
        symbol: RawStock(**stock_data)
        for symbol, stock_data in extracted_data.items()
        if TimeFunctionsMap[TimeFunctions.TIME_SERIES_WEEKLY] in stock_data
    }
