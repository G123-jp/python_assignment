from pydantic import BaseModel, validator
from typing import List, Any, Optional
from decimal import Decimal
from datetime import date


class FinancialData(BaseModel):
    symbol: str
    date: str
    open_price: str
    close_price: str
    volume: str

    @validator('date', pre=True, always=True)
    def date_to_str(cls, value):
        if isinstance(value, date):
            return value.isoformat()
        return value

    @validator('open_price', 'close_price', 'volume')
    def convert_to_string(cls, v):
        return str(v)

    class Config:
        orm_mode = True


class Pagination(BaseModel):
    count: int
    page: int
    limit: int
    pages: int

    class Config:
        orm_mode = True


class CreateFinancialData(BaseModel):
    symbol: str
    date: str
    open_price: str
    close_price: str
    volume: str


class GetFinancialDataResponse(BaseModel):
    data: List[FinancialData]
    pagination: Pagination
    info: Any

    class Config:
        orm_mode = True


class StatisticsData(BaseModel):
    start_date: str
    end_date: str
    symbol: str
    average_daily_open_price: float
    average_daily_close_price: float
    average_daily_volume: int

    class Config:
        orm_mode = True


class GetStatisticsDataResponse(BaseModel):
    data: StatisticsData
    info: Any

    class Config:
        orm_mode = True
