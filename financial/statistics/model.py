""" Model class for Statistics """
from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel


class Statistics(BaseModel):
    start_date: Optional[str] = ""
    end_date: Optional[str] = ""
    symbol: str
    average_daily_open_price: float
    average_daily_close_price: float
    average_daily_volume: int

    def __init__(__pydantic_self__, **data: Any) -> None:
        super().__init__(**data)


async def calculate_statistics(**data):
    """Calculates statistics for financial data"""
    finanical_data = data.get("results", [])
    open_prices = [float(stock["open_price"]) for stock in finanical_data]
    data["average_daily_open_price"] = sum(open_prices) / len(open_prices)
    close_prices = [float(stock["close_price"]) for stock in finanical_data]
    data["average_daily_close_price"] = sum(close_prices) / len(close_prices)
    volumes = [int(stock["volume"]) for stock in finanical_data]
    data["average_daily_volume"] = sum(volumes) / len(volumes)
    return Statistics(**data)
