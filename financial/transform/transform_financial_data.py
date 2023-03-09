""" Model class for Transforming Finanical Data"""

from __future__ import annotations

from datetime import datetime
from typing import Dict, List

from pydantic import BaseModel, validate_arguments

from financial.extract.extract import RawStock


class FinancialData(BaseModel):
    symbol: str
    date: datetime
    open_price: float
    close_price: float
    volume: int


def _transform(symbol, timeseries_data) -> List[FinancialData]:
    """Helper function for transofrm finanical data"""
    financial_data: List[FinancialData] = [
        FinancialData(
            **dict(
                symbol=symbol,
                date=data.timestamp,
                open_price=float(data.open),
                close_price=float(data.close),
                volume=int(data.volume),
            ),
        )
        for data in timeseries_data
    ]
    return financial_data


@validate_arguments
def transform(stock_data: Dict[str, RawStock]) -> List[FinancialData]:
    """
    Transform RawStockbData in Required format
    Args:
        stock_data (Dict[str, RawStock])
    Returns:
        List[FinancialData]: List of FinancialData
    """
    financial_data: List[FinancialData] = []
    for symbol, raw_stock in stock_data.items():
        financial_data.extend(_transform(symbol, raw_stock.TimeSeries))
    return financial_data
